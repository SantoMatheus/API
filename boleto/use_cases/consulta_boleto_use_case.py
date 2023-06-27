import uuid

from boleto.models import Boleto
from conta.use_cases.buscar_conta_por_agencia_use_case import BuscarContaPorAgenciaUseCase


class ConsultaBoletoUseCase:

    def __init__(self):
        self.buscar_conta_por_agencia_use_case = BuscarContaPorAgenciaUseCase()

    def execute(self, agencia: str, num_conta: str, id_boleto: uuid):
        conta_corrente = self.buscar_conta_por_agencia_use_case.execute(agencia=agencia, num_conta=num_conta)
        boleto = Boleto.objects.get(conta_corrente=conta_corrente, id=id_boleto)
        return boleto