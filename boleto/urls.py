from django.urls import path

from boleto.views import GerarBoletoView, ConsultaBoletosView, PagarBoletoView, CancelarBoletoView

app_name = 'boleto'

urlpatterns =[
    path('boleto/gerarboleto', GerarBoletoView.as_view()),
    path('boleto/listar', ConsultaBoletosView.as_view()),
    path('boleto/pagamento/<str:agencia>/<str:num_conta>', PagarBoletoView.as_view()),
    path('boleto/cancelamento/<str:agencia>/<str:num_conta>', CancelarBoletoView.as_view())

]