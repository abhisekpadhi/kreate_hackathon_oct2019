from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
]