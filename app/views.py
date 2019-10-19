# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.forms import model_to_dict
from django.views.generic.base import TemplateView
from .models import *
from urllib.parse import urlencode, quote_plus
from pprint import pprint
import datetime
import json
from app.LoginManager import LoginManager
from app.OrderManager import OrderManager
from app.EncryptionManager import EncryptionManager
from app.OTPManager import OTPManager
from app.UserManager import UserManager
from base64 import b64decode, b64encode


class HomePageView(View):
    def __init__(self):
        super().__init__()
        self.login_manager = LoginManager()

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        phone = request.POST.get('collector_phone')
        if phone:
            logged_in_user = self.login_manager.login_by_phone(phone)
            request.session['login_id'] = logged_in_user.id
            return redirect(reverse('orders'))
        else:
            return render(request, "index.html")


class OrdersView(View):
    def __init__(self):
        super().__init__()
        self.order_manager = OrderManager()
        self.encryption_manager = EncryptionManager()
        self.otp_manager = OTPManager()
        self.user_manager = UserManager()

    def get(self, request, order_id=None):
        login_id = request.session.get('login_id', None)

        if not login_id:
            redirect(reverse('home'))

        if not order_id:
            pickups = self.order_manager.get_all_orders_for_collector(login_id)
            context = {
                "pickups": pickups if pickups else []
            }
            return render(request, "orders.html", context)

        if order_id:
            order = self.order_manager.get_order_by_id(order_id=order_id)
            if order:
                payable = self.order_manager.get_payable_by_order(order)
                context = {
                    "order": order,
                    "payable": payable
                }
                return render(request, "order.html", context)
            else:
                return redirect(reverse('orders'))

    def post(self, request, order_id=None):
        login_id = request.session.get('login_id', None)

        if not login_id:
            redirect(reverse('home'))

        if order_id:
            if request.POST.get('action') == 'start_transaction':
                payable = request.POST.get('payable')
                if not payable:
                    return redirect(reverse('orders'))
                context = {
                    "payable": int(payable),
                    "order_id": order_id,
                    "user_id": login_id
                }
                return render(request, "transact.html", context)

            if request.POST.get('action') == 'start_verification':
                order_id = request.POST.get('order_id')
                payable = request.POST.get('payable')
                user_id = request.POST.get('user_id')

                if order_id and payable and user_id:
                    data = f"{order_id}.{payable}.{user_id}"

                    print(data)

                    ciphertext = self.encryption_manager.get_encrypted_cipher(
                        user_id=int(user_id),
                        data=data
                    )

                    plaintext = self.encryption_manager.get_decrypt_cipher(
                        user_id=user_id,
                        ciphertext=ciphertext
                    )

                    otp = self.encryption_manager.get_otp_string()

                    data = f"{plaintext.decode()}.{otp}"

                    signature = self.encryption_manager.get_signature(
                        data=data,
                        user_id=user_id
                    )
                    print(f'generated: {signature}')

                    otp_message = f"Your OTP is - {otp}"
                    # self.otp_manager.send_otp(
                    #     data=otp_message,
                    #     to=[self.user_manager.get_user_by_id(user_id).phone]
                    # )
                    print(f'otp_message: {otp_message}')

                    context = {
                        "order_id": order_id,
                        "payable": payable,
                        "user_id": user_id,
                        "cipher": b64encode(ciphertext).decode(),
                        "signature": b64encode(signature).decode()
                    }
                    return render(request, "verify.html", context)
                else:
                    return redirect(reverse('orders'))

            if request.POST.get('action') == 'start_otp_validation':
                otp = request.POST.get('otp')
                order_id = request.POST.get('order_id')
                payable = request.POST.get('payable')
                user_id = request.POST.get('user_id')
                signature = request.POST.get('signature')
                print(f'Received: {b64decode(signature)}')

                data = f"{order_id}.{payable}.{user_id}.{otp}"


                # signature = self.encryption_manager.get_signature(
                #     data=data,
                #     user_id=user_id
                # )

                is_verified = self.encryption_manager.is_data_verified(
                    data=data,
                    signature=b64decode(signature),
                    user_id=user_id
                )

                if is_verified:
                    return render(request, "success.html")

                else:
                    return redirect(reverse('orders'))



