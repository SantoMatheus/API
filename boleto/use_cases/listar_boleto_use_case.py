from boleto.models import Boleto
from conta.models import ContaCorrente


class ListarBoletoUseCase:

    def execute(self, agencia=None, id_conta=None, status=None, id_boleto=None):
        parametros_conta = {}
        if agencia:
            parametros_conta['agencia'] = agencia
        if id_conta:
            parametros_conta['id'] = id_conta
        contas_correntes = ContaCorrente.objects.filter(**parametros_conta)

        parametros_boleto = {}
        if status:
            parametros_boleto['status'] = status
        if id_boleto:
            parametros_boleto['id'] = id_boleto
        boletos = Boleto.objects.filter(conta_corrente__in=contas_correntes, **parametros_boleto)

        return boletos
