from conta.models import Deposito


class BuscarDepositoUseCase:
    def execute(self, agencia: str, num_conta: str):
        return Deposito.objects.filter(conta_corrente__agencia=agencia, conta_corrente__num_conta=num_conta)
