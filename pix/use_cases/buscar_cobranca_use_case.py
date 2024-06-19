from pix.models import TransferenciaPix


class BuscarCobrancaPixUseCase:
    def execute(self, chave_pix: str):
        return TransferenciaPix.objects.filter(conta_destino__valor_chave=chave_pix)

