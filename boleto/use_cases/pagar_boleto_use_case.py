import uuid

from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.use_cases.consulta_boleto_use_case import ConsultaBoletoUseCase


class PagarBoletoUseCase:

    def __init__(self):
        self.consulta_boleto_use_case = ConsultaBoletoUseCase()

    def execute(self, id_boleto: uuid, num_conta: str, agencia: str):
        boleto = self.consulta_boleto_use_case.execute(id_boleto=id_boleto, num_conta=num_conta, agencia=agencia)
        saldo = boleto.conta_corrente.saldo
        pagamento = boleto.valor

        if boleto.pago is True:
            raise BoletoPago('Boleto já liquidado.')

        if saldo <= pagamento:
            raise SaldoInsuficiente('Saldo insuficiente para este pagamento.')

        boleto.conta_corrente.saldo -= pagamento
        boleto.pago = True
        boleto.save()
        boleto.conta_corrente.save()
        return boleto
