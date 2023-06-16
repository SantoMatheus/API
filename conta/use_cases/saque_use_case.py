from conta.exceptions.agencia_invalido import AgenciaInvalido
from conta.exceptions.agencia_is_None import AgenciaNulo
from conta.exceptions.num_conta_invalido import NumContaInvalido
from conta.exceptions.num_conta_is_none import NumContaNulo
from conta.exceptions.saldo_insuficiente import SaldoInsuficiente
from conta.use_cases.buscar_conta_por_agencia_use_case import BuscarContaPorAgenciaUseCase


class SaqueUseCase:

    def __init__(self):
        self.buscar_conta_por_agencia_use_case = BuscarContaPorAgenciaUseCase()

    def execute(self, agencia: str, num_conta: str, valor_saque: float):
        conta_corrente = self.buscar_conta_por_agencia_use_case.execute(agencia=agencia, num_conta=num_conta)

        if conta_corrente.saldo < valor_saque:
            raise SaldoInsuficiente('Saldo insuficiente para a operação desejada.')

        conta_corrente.saldo -= valor_saque
        conta_corrente.save()
        return conta_corrente

