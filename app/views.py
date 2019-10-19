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
                    "payable": int(payable)
                }
                return render(request, "transact.html", context)

            if request.POST.get('action') == 'start_verification':
                pass
