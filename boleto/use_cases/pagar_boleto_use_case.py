import uuid

from rest_framework.exceptions import ValidationError

from boleto.exceptions import SaldoInsuficiente
from boleto.models import PagamentoBoleto
from boleto.use_cases.consulta_boleto_por_id_use_case import ConsultaBoletoPorIdUseCase
from boleto.use_cases.listar_boleto_use_case import ListarBoletoUseCase
from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase


class PagarBoletoUseCase:

    def __init__(self):
        self.consulta_boleto_por_id_use_case = ConsultaBoletoPorIdUseCase()
        self.consultar_conta_use_case = BuscarContaUseCase()

    def execute(self, id_boleto: uuid.UUID, conta_sacado: str, agencia_sacado: str):
        conta_sacado = self.consultar_conta_use_case.execute(num_conta=conta_sacado, agencia=agencia_sacado)
        boleto = self.consulta_boleto_por_id_use_case.execute(id_boleto=id_boleto)
        pagamento = boleto.valor

        status_erros = {
            'vencido': 'Não é possível realizar o pagamento de cobranças vencidas.',
            'pago': 'Pagamento já efetuado.',
            'cancelado': 'Não é possível realizar o pagamento de cobranças canceladas.'
        }

        if boleto.status in status_erros:
            raise ValidationError({'Status': status_erros[boleto.status]})

        if conta_sacado.saldo < pagamento:
            raise SaldoInsuficiente('Saldo insuficiente para este pagamento.')

        boleto.conta_corrente.saldo += pagamento
        conta_sacado.saldo -= pagamento
        boleto.status = "pago"
        boleto.save()
        boleto.conta_corrente.save()
        conta_sacado.save()
        pagamento = PagamentoBoleto.objects.create(boleto=boleto, conta_sacado=conta_sacado)
        return pagamento
