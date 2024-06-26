from rest_framework.exceptions import ValidationError

from boleto.models import PagamentoBoleto


class BuscarPagamentoBoletoUseCase:
    def execute(self, agencia_sacado: str, num_conta_sacado: str):
        if not agencia_sacado or num_conta_sacado:
            raise ValidationError('Informar agência e conta corrente do sacado.')

        pagamento_boleto = PagamentoBoleto.objects.filter(conta_sacado__agencia=agencia_sacado,
                                                          conta_sacado__num_conta=num_conta_sacado)
        return pagamento_boleto
