from boleto.models import Boleto
from conta.models import ContaCorrente


class ListarBoletoUseCase:

    def execute(self, agencia=None, num_conta=None, pago=None, id_boleto=None):
        parametros_conta = {}
        if agencia:
            parametros_conta['agencia'] = agencia
        if num_conta:
            parametros_conta['num_conta'] = num_conta
        contas_correntes = ContaCorrente.objects.filter(**parametros_conta)

        parametros_boleto = {}
        if pago:
            parametros_boleto['pago'] = pago
        if id_boleto:
            parametros_boleto['id'] = id_boleto
        boletos = Boleto.objects.filter(conta_corrente__in=contas_correntes, **parametros_boleto)

        return boletos