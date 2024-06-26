from django.urls import path

from boleto.views import GerarBoletoView, ListarBoletosView, PagarBoletoView, CancelarBoletoView, \
    ConsultaBoletoPorIdView, BuscarPagamentoBoletoView, BuscarRecebimentoBoletoView

app_name = 'boleto'

urlpatterns = [
    path('boletos/gerar_boleto', GerarBoletoView.as_view()),
    path('boletos/listar', ListarBoletosView.as_view(), name='listar_boletos'),
    path('boletos/consultar/', ConsultaBoletoPorIdView.as_view()),
    path('boletos/pagamento/<str:agencia_sacado>/<str:conta_sacado>', PagarBoletoView.as_view()),
    path('boletos/cancelamento/', CancelarBoletoView.as_view()),
    path('boletos/buscar_pagamento_boleto/', BuscarPagamentoBoletoView.as_view()),
    path('boletos/buscar_recebimento_boleto/', BuscarRecebimentoBoletoView.as_view()),
]
