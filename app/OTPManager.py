import requests
from OfflineCashCollector import settings
from urllib.parse import urlencode, quote_plus


class OTPManager:
    @staticmethod
    def send_otp(data, to):
        sms = [
            {
                "message": quote_plus(data.lstrip().rstrip()),
                "to": to
            }
        ]

        try:
            sms_client = MSG91()
            sms_client.prepare(sms=sms)
            sms_client.send()

            if sms_client.response.status_code != 200:
                raise Exception
            else:
                print(f'SMS Send Status: {sms_client.response.status_code}')
        except:
            print("Failed to send sms.")


class MSG91:
    def __init__(self):
        '''
        Instantiates a msg91 object
        '''
        self.url = settings.MSG91_API_URL
        self.headers = {
            "authkey": settings.MSG91_AUTH_KEY,
            "content-type": "application/json"
        }

    def prepare(self, sms):
        '''
        Prepares payload for sms.
        `sender` has to be 6 char word
        :param sms: list of dict of `message` and `to`
        :return: nothing
        sms = [
                {
                    "message": "Testing msg91",
                    "to": ["9437023567"]
                },
            ]
        '''
        self.payload = {
            "sender": settings.MSG91_SENDER_ID,
            "route": settings.MSG91_ROUTE,
            "country": settings.MSG91_COUNTRY,
            "sms": sms
        }

    def send(self):
        '''
        Triggers the sms.
        :return: requests `response` object
        '''
        self.response = requests.post(
            url=self.url,
            json=self.payload,
            headers=self.headers
        )
        # return self.response


# if __name__ == "__main__":
#     otp = OTPManager()
#     otp.send_otp(
#         data="1234",
#         to=["9439831236"]
#     )