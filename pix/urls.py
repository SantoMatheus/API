from django.urls import path

from pix.views import CriarChavePixView

app_name = 'pix'

urlpatterns = [
    path('pix/criar_chave_pix/<str:agencia>/<str:num_conta>', CriarChavePixView.as_view())
    ]
