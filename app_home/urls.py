from django.contrib import admin
from django.urls import path

from app_home.views import Home

urlpatterns = [
    path("", Home, name="home"),
]
