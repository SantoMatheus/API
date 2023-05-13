from django.urls import path

from conta.views import (CriarContaView, ConsultarContaView, DepositoView, SaqueView, TransferenciaView,
                         MulticontaView, IdealConsultaContaView)

app_name = 'conta'

urlpatterns = [
    path('conta/create', CriarContaView.as_view()),
    path('conta/get', ConsultarContaView.as_view()),
    path('conta/deposito/<str:agencia>/<str:num_conta>', DepositoView.as_view()),
    path('conta/saque/<str:agencia>/<str:num_conta>', SaqueView.as_view()),
    path('conta/transfer/', TransferenciaView.as_view()),
    path('conta/multiconta/', MulticontaView.as_view()),
    path('conta/ideal/retrieve/<str:agencia>/<str:conta>/', IdealConsultaContaView.as_view()),
]
