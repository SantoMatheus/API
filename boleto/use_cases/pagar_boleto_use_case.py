import uuid

from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.use_cases.consulta_boleto_use_case import ConsultarBoletoUseCase


class PagarBoletoUseCase:

    def __init__(self):
        self.consulta_boleto_use_case = ConsultarBoletoUseCase()

    def execute(self, id_boleto: uuid.UUID):
        boleto = self.consulta_boleto_use_case.objects.get(id_boleto=id_boleto)
        saldo = boleto.conta_corrente.saldo
        pagamento = boleto.valor

        if boleto.pago is True:
            raise BoletoPago('Boleto já liquidado.')

        if saldo < pagamento:
            raise SaldoInsuficiente('Saldo insuficiente para este pagamento.')

        boleto.conta_corrente.saldo -= pagamento
        boleto.pago = True
        boleto.save()
        boleto.conta_corrente.save()
        return boleto
