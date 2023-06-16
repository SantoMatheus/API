from conta.exceptions.agencia_invalido import AgenciaInvalido
from conta.exceptions.agencia_is_None import AgenciaNulo
from conta.exceptions.num_conta_invalido import NumContaInvalido
from conta.exceptions.num_conta_is_none import NumContaNulo
from conta.exceptions.saldo_insuficiente import SaldoInsuficiente
from conta.use_cases.buscar_conta_por_agencia_use_case import BuscarContaPorAgenciaUseCase


class DepositoUseCase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_conta_por_agencia_use_case = BuscarContaPorAgenciaUseCase()

    def execute(self, agencia: str, num_conta: str, valor_deposito: float):
        conta_corrente = self.buscar_conta_por_agencia_use_case.execute(agencia=agencia, num_conta=num_conta)

        if agencia is None:
            raise AgenciaNulo('Informe um número de agencia.')
        if num_conta is None:
            raise NumContaNulo('Informe um número de conta.')
        if agencia is not True:
            raise AgenciaInvalido('Informe um número de agencia válido.')
        if num_conta is not True:
            raise NumContaInvalido('Informe um número de conta válido.')
        if conta_corrente.saldo < valor_deposito:
            raise SaldoInsuficiente('Saldo insuficiente para a operação desejada.')

        conta_corrente.saldo += valor_deposito
        conta_corrente.save()
        return conta_corrente
