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


class HomePageView(View):
    def get(self, request):
        return render(request, "index.html")