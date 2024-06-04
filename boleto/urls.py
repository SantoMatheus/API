from django.urls import path

from boleto.views import GerarBoletoView, ListarBoletosView, PagarBoletoView, CancelarBoletoView, ConsultarBoletoView

app_name = 'boleto'

urlpatterns = [
    path('boleto/gerarboleto', GerarBoletoView.as_view()),
    path('boleto/listar', ListarBoletosView.as_view()),
    path('boleto/consultar/<str:id_boleto>', ConsultarBoletoView.as_view()),
    path('boleto/pagamento/<str:id_boleto>', PagarBoletoView.as_view()),
    path('boleto/cancelamento/<str:id_boleto>', CancelarBoletoView.as_view())
]
