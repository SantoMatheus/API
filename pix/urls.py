from django.urls import path

from pix.views import CriarChavePixView, ConsultarChavesPixPorContaView, ConsultarChavePixPeloHashView, \
    ExcluirChavePixView, CriarCobrancaPixView, PagarPixView, BuscarCobrancaPixView

app_name = 'pix'

urlpatterns = [
    path('pix/criar_chave_pix/<str:agencia>/<str:num_conta>', CriarChavePixView.as_view()),
    path('pix/consultar_chave_pix_por_dados_bancarios/', ConsultarChavesPixPorContaView.as_view()),
    path('pix/consultar_chave_pix_por_hash/', ConsultarChavePixPeloHashView.as_view()),
    path('pix/excluir_chave_pix/', ExcluirChavePixView.as_view()),
    path('pix/buscar_cobranca_pix/', BuscarCobrancaPixView.as_view()),
    path('pix/criar_cobranca_pix/', CriarCobrancaPixView.as_view()),
    path('pix/pagamento_pix/', PagarPixView.as_view()),
    ]
