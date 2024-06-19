from boleto.models import Boleto
from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase


class GerarBoletoUseCase:

    def __init__(self):
        self.buscar_conta_por_agencia_use_case = BuscarContaUseCase()

    def execute(self, agencia: str, num_conta: str, valor: str, data_vencimento: str):
        conta_corrente = self.buscar_conta_por_agencia_use_case.execute(agencia=agencia, num_conta=num_conta)
        boleto = Boleto.objects.create(conta_corrente=conta_corrente, valor=valor, data_vencimento=data_vencimento)
        return boleto
