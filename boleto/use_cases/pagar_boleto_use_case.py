import uuid

from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.use_cases.consulta_boleto_por_id_use_case import ConsultaBoletoPorIdUseCase
from conta.use_cases.buscar_conta_por_agencia_use_case import BuscarContaPorAgenciaUseCase


class PagarBoletoUseCase:

    def __init__(self):
        self.consulta_boleto_por_id_use_case = ConsultaBoletoPorIdUseCase()
        self.consultar_conta_use_case = BuscarContaPorAgenciaUseCase()

    def execute(self, id_boleto: uuid.UUID, num_conta_sacado: str, agencia_sacado: str):
        conta_sacado = self.consultar_conta_use_case.execute(num_conta=num_conta_sacado, agencia=agencia_sacado)
        boleto = self.consulta_boleto_por_id_use_case.execute(id_boleto=id_boleto)
        pagamento = boleto.valor

        if boleto.pago is True:
            raise BoletoPago('Boleto já liquidado.')

        if conta_sacado.saldo < pagamento:
            raise SaldoInsuficiente('Saldo insuficiente para este pagamento.')

        boleto.conta_corrente.saldo += pagamento
        conta_sacado.saldo -= pagamento
        boleto.pago = True
        boleto.status = "Pago"
        boleto.save()
        boleto.conta_corrente.save()
        conta_sacado.save()
        return boleto
