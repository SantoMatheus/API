from django.contrib import admin
from django.urls import path

from conta.views import CriarContaView, ConsultarContaView

app_name = 'conta'

urlpatterns = [
    path('conta/create', CriarContaView.as_view()),
    path('conta/get/<str:agencia>/<str:num_conta>', ConsultarContaView.as_view()),

]