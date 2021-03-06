from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode, b64decode
from app.UserManager import UserManager
from OfflineCashCollector import settings
import random


class EncryptionManager:
    def __init__(self):
        self.public_exponent = 65537
        self.key_size = 512
        self.user_manager = UserManager()
        self.otp_length = 4

    def generate_key_pair_for_user(self, user_id):
        private_key = rsa.generate_private_key(
            public_exponent=self.public_exponent,
            key_size=self.key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        user = self.user_manager.get_user_by_id(user_id=user_id)
        print(type(user))
        if user:
            user.privkey = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()

            user.pubkey = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

            user.save()

    def get_private_key_by_user_id(self, user_id):
        # user = self.user_manager.get_user_by_id(user_id=user_id)
        # if not user.privkey:
        #     self.generate_key_pair_for_user(user_id=user.id)
        #     user = self.user_manager.get_user_by_id(user_id=user_id)

        with open(settings.PRIVKEY, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        
        return private_key

    def get_public_key_by_user_id(self, user_id):
        private_key = self.get_private_key_by_user_id(user_id)
        return private_key.public_key()

    def get_encrypted_cipher(self, user_id, data):
        public_key = self.get_public_key_by_user_id(user_id)
        ciphertext = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return ciphertext

    def get_decrypt_cipher(self, user_id, ciphertext):
        private_key = self.get_private_key_by_user_id(user_id)
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return plaintext

    def get_otp_string(self):
        otp = ""
        for _ in range(self.otp_length):
            otp += str(random.randint(1, 9))
        return otp

    def get_signature(self, data, user_id):
        private_key = self.get_private_key_by_user_id(user_id)
        signature = private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA1()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA1()
        )
        return signature

    def get_encoded_signature(self, signature):
        return b64encode(signature)

    def get_decoded_signature(self, signature):
        return b64decode(signature)

    def is_data_verified(self, data, signature, user_id):
        public_key = self.get_public_key_by_user_id(user_id)
        print(type(signature))
        try:
            public_key.verify(
                signature,
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA1()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA1()
            )
            return True
        except Exception as e:
            print(e)
            return False




# if __name__ == '__main__':
    # print(private_key.private_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PrivateFormat.TraditionalOpenSSL,
    #     encryption_algorithm=serialization.NoEncryption()
    # ).decode())
    #
    # print(public_key.public_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PublicFormat.SubjectPublicKeyInfo
    # ).decode())

    # collector
    # data = "1.1000.1"
    # ciphertext = public_key.encrypt(
    #     data.encode(),
    #     padding.OAEP(
    #         mgf=padding.MGF1(algorithm=hashes.SHA1()),
    #         algorithm=hashes.SHA1(),
    #         label=None
    #     )
    # )
    # print(len(ciphertext))
    # print(ciphertext)

    # server
    # plaintext = private_key.decrypt(
    #     ciphertext,
    #     padding.OAEP(
    #         mgf=padding.MGF1(algorithm=hashes.SHA1()),
    #         algorithm=hashes.SHA1(),
    #         label=None
    #     )
    # )
    # print(plaintext.decode())

    # buyer
    #otp = '1234'

    # server
    # data_with_otp = plaintext.decode()+'.'+otp
    # print(data_with_otp)
    #
    # signature = private_key.sign(
    #     data_with_otp.encode(),
    #     padding.PSS(
    #         mgf=padding.MGF1(hashes.SHA1()),
    #         salt_length=padding.PSS.MAX_LENGTH
    #     ),
    #     hashes.SHA1()
    # )

    # encoded_signature = b64encode(signature)
    # print(encoded_signature)
    # print(len(encoded_signature))

    # collector
    # new_data = data+'.'+otp
    # print(new_data)
    #
    # verify = public_key.verify(
    #     signature,
    #     new_data.encode(),
    #     padding.PSS(
    #         mgf=padding.MGF1(hashes.SHA1()),
    #         salt_length=padding.PSS.MAX_LENGTH
    #     ),
    #     hashes.SHA1()
    # )
    # print(verify)

