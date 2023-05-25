from django.urls import path

from transferencia.views import TransferenciaView, ConsultaTransferenciaView

app_name = 'transferencia'

urlpatterns =[
    path('transferencia/<str:agencia>/<str:num_conta>', TransferenciaView.as_view()),
    path('consulta/<uuid:id_transferencia>', ConsultaTransferenciaView.as_view())
    ]