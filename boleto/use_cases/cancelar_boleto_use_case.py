import uuid

from rest_framework import status
from rest_framework.exceptions import ValidationError

from boleto.use_cases.consulta_boleto_por_id_use_case import ConsultaBoletoPorIdUseCase


class CancelarBoletoUseCase:

    def __init__(self):
        self.consulta_boleto_use_case = ConsultaBoletoPorIdUseCase()

    def execute(self, id_boleto: uuid.UUID):
        status_erros = {
            'vencido': 'Não é possível realizar o cancelamento de cobranças vencidas.',
            'pago': 'Pagamento já efetuado.',
            'cancelado': 'O status atual do boleto já é cancelado.'
        }

        boleto = self.consulta_boleto_use_case.execute(id_boleto=id_boleto)

        if boleto.status in status_erros:
            raise ValidationError({'Status': status_erros[boleto.status]})

        boleto.status = "Cancelado"
        boleto.save()
        boleto.conta_corrente.save()
        return boleto
