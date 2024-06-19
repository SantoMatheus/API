from django.urls import path

from conta.views import (CriarContaView, DepositoView, SaqueView,
                         MulticontaView, ListarContaView, ListarTransferenciaView, TransferenciaView, CancelarContaView)

app_name = 'conta'

urlpatterns = [
    path('conta/create', CriarContaView.as_view()),
    path('conta/deposito/<str:agencia>/<str:num_conta>', DepositoView.as_view()),
    path('conta/saque/<str:agencia>/<str:num_conta>', SaqueView.as_view()),
    path('conta/multiconta/', MulticontaView.as_view()),
    path('conta/listar/', ListarContaView.as_view()),
    path('conta/transferencia/<str:agencia>/<str:num_conta>', TransferenciaView.as_view()),
    path('conta/listar/', ListarTransferenciaView.as_view()),
    path('conta/cancelar/', CancelarContaView.as_view()),
]
