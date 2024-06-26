from typing import Optional

from django.db.models import Q

from pix.models import DevolucaoPix


class BuscarDevolucaoPixUseCase:
    def execute(self, agencia: Optional[str] = None, num_conta: Optional[str] = None):

        devolucao = DevolucaoPix.objects.filter(
            pagamento__cobranca_pix__conta_destino__conta_corrente__agencia=agencia,
            pagamento__cobranca_pix__conta_destino__conta_corrente__num_conta=num_conta)
        return devolucao
