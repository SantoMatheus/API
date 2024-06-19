from conta.models import Deposito
from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase


class DepositoUseCase:

    def __init__(self):
        self.buscar_conta_por_agencia_use_case = BuscarContaUseCase()

    def execute(self, agencia: str, num_conta: str, valor_deposito: float):
        conta_corrente = self.buscar_conta_por_agencia_use_case.execute(agencia=agencia, num_conta=num_conta)

        conta_corrente.saldo += valor_deposito
        conta_corrente.save()

        return Deposito.objects.create(conta_corrente=conta_corrente, valor=valor_deposito)
