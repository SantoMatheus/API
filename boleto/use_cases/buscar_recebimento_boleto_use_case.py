from rest_framework.exceptions import ValidationError

from boleto.models import PagamentoBoleto


class BuscarRecebimentoBoletoUseCase:
    def execute(self, agencia_cedente: str, num_conta_cedente: str):
        if not agencia_cedente or num_conta_cedente:
            raise ValidationError('Informar agência e conta corrente do cedente.')

        recebimento_boleto = PagamentoBoleto.objects.filter(boleto__conta_corrente__agencia=agencia_cedente,
                                                            boleto__conta_corrente__num_conta=num_conta_cedente)
        return recebimento_boleto
