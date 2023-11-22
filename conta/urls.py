from django.urls import path

from conta.views import (CriarContaView, DepositoView, SaqueView,
                         MulticontaView, ListarContaView)

app_name = 'conta'

urlpatterns = [
    path('conta/create', CriarContaView.as_view()),
    path('conta/deposito/<str:agencia>/<str:num_conta>', DepositoView.as_view()),
    path('conta/saque/<str:agencia>/<str:num_conta>', SaqueView.as_view()),
    path('conta/multiconta/', MulticontaView.as_view()),
    path('conta/listar/', ListarContaView.as_view()),
]
