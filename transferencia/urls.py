from django.urls import path

from transferencia.views import TransferenciaView, ConsultaTransferenciaView

app_name = 'transferencia'

urlpatterns =[
    path('transferencia/<str:agencia>/<str:num_conta>', TransferenciaView.as_view()),
    path('transferencia/<str:agencia_origem>/<str:num_conta_origem>/consulta/<uuid:id_transferencia>/',
         ConsultaTransferenciaView.as_view())
    ]