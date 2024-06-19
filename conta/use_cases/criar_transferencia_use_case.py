from rest_framework.exceptions import ValidationError

from conta.models import Transferencia
from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase
from conta.use_cases.deposito_use_case import DepositoUseCase
from conta.use_cases.saque_use_case import SaqueUseCase


class CriarTransferenciaUseCase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_conta_use_case = BuscarContaUseCase()

    def execute(self, agencia_origem: str, num_conta_origem: str, agencia_destino: str, num_conta_destino: str,
                valor: float):
        conta_origem = self.buscar_conta_use_case.execute(agencia=agencia_origem, num_conta=num_conta_origem)
        # Busca a conta que irá originar a transferência
        if conta_origem.saldo < valor:
            raise ValidationError({'Saldo': 'Saldo insuficiente para a operação solicitada.'})

        # Busca a conta que irá receber a transferência
        conta_destino = self.buscar_conta_use_case.execute(agencia=agencia_destino, num_conta=num_conta_destino)

        # Desconta o valor da transferñcia da conta de origem
        conta_origem.saldo -= valor
        conta_origem.save()

        # Credita o valor da transferñcia na conta de destino
        conta_destino.saldo += valor
        conta_destino.save()

        # Cria o objeto transferência
        return Transferencia.objects.create(conta_origem=conta_origem, conta_destino=conta_destino,
                                            valor=valor)
