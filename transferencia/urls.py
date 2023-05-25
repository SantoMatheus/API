from django.urls import path

from transferencia.views import TransferenciaView

app_name = 'transferencia'

urlpatterns =[
    path('transferencia/<str:agencia>/<str:num_conta>', TransferenciaView.as_view())
    ]