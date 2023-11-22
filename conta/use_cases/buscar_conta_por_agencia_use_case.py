from conta.models import ContaCorrente


class BuscarContaPorAgenciaUseCase:

    def execute(self, agencia: str, num_conta: str):
        conta_corrente = ContaCorrente.objects.get(agencia=agencia, num_conta=num_conta)
        return conta_corrente
