from conta.exceptions.agencia_invalido import AgenciaInvalido
from conta.exceptions.agencia_is_None import AgenciaNulo
from conta.exceptions.num_conta_invalido import NumContaInvalido
from conta.exceptions.num_conta_is_none import NumContaNulo
from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase
from conta.use_cases.criar_conta_use_case import CriarContaUseCase


class MulticontaUseCase:

    def __init__(self):
        self.buscar_conta_por_agencia_use_case = BuscarContaUseCase()
        self.criar_conta_use_case = CriarContaUseCase()

    def execute(self, agencia: str, num_conta: str):
        conta_corrente_existente = self.buscar_conta_por_agencia_use_case.execute(agencia=agencia, num_conta=num_conta)

        nova_conta = self.criar_conta_use_case.execute(nome=conta_corrente_existente.nome,
                                                       cpf=conta_corrente_existente.cpf)
        return nova_conta
