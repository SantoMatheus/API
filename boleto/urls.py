from django.urls import path

from boleto.views import GerarBoletoView, ListarBoletosView, PagarBoletoView, CancelarBoletoView, \
    ConsultaBoletoPorIdView

app_name = 'boleto'

urlpatterns = [
    path('boletos/gerar_boleto', GerarBoletoView.as_view()),
    path('boletos/listar', ListarBoletosView.as_view(), name='listar_boletos'),
    path('boletos/consultar/', ConsultaBoletoPorIdView.as_view()),
    path('boletos/pagamento/<str:num_conta_sacado>/<str:agencia_sacado>', PagarBoletoView.as_view()),
    path('boletos/cancelamento/', CancelarBoletoView.as_view())
]
