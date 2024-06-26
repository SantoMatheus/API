from django.urls import path

from extrato.views import BuscarEventosView

app_name = 'extrato'

urlpatterns = [
    path('extrato/create/', BuscarEventosView.as_view()),
]
