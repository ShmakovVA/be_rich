from django.contrib import admin
from django.urls import path

from backend.api.views import login, register, test

urlpatterns = [
    path('login', login),
    path('register', register),
    path('test', test),
]
