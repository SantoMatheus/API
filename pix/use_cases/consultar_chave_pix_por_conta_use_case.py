from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase
from pix.models import ChavePix


class ConsultarChavePixPorContaUseCase:

    def execute(self, agencia: str, num_conta: str):
        chave_pix = ChavePix.objects.filter(conta_corrente__agencia=agencia, conta_corrente__num_conta=num_conta)
        return chave_pix
