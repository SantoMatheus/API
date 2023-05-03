from django.urls import path

from boleto.views import GerarBoletoView

app_name = 'boleto'

urlpatterns =[
    path('boleto/gerarboleto/', GerarBoletoView.as_view())
]