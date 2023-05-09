from conta.models import ContaCorrente
from conta.repositories import ContaCorrenteRepository


class ConsultarContaUseCase:
    def __init__(self, conta_corrente_repository: ContaCorrenteRepository):
        self._conta_corrente_repository = conta_corrente_repository

    def execute(self, agencia: str, conta: str) -> ContaCorrente:
        conta_corrente = self.__find_in_db(agencia=agencia, conta=conta)
        return conta_corrente

    def __find_in_db(self, agencia: str, conta: str):
        return self._conta_corrente_repository.find_by_agencia_and_conta(agencia=agencia, conta=conta)
