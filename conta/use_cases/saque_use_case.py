from rest_framework.exceptions import ValidationError

from conta.models import Saque
from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase


class SaqueUseCase:

    def __init__(self):
        self.buscar_conta_por_agencia_use_case = BuscarContaUseCase()

    def execute(self, agencia: str, num_conta: str, valor_saque: float):
        conta_corrente = self.buscar_conta_por_agencia_use_case.execute(agencia=agencia, num_conta=num_conta)

        if conta_corrente.saldo < valor_saque:
            raise ValidationError({'Saldo': 'Saldo insuficiente para a operação desejada.'})

        conta_corrente.saldo -= valor_saque
        conta_corrente.save()
        return Saque.objects.create(conta_corrente=conta_corrente,
                                    valor=valor_saque)
