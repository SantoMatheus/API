from django.contrib import admin
from django.urls import path

from conta.views import CriarContaView

app_name = 'conta'

urlpatterns = [
    path('conta/create', CriarContaView.as_view())
]