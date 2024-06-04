import uuid

from boleto.use_cases.consulta_boleto_use_case import ConsultarBoletoUseCase


class CancelarBoletoUseCase:

    def __init__(self):
        self.consulta_boleto_use_case = ConsultarBoletoUseCase()

    def execute(self, id_boleto: uuid.UUID):
        boleto = self.consulta_boleto_use_case.objects.get(id_boleto=id_boleto)
        boleto.status = "Cancelado"
        boleto.save()
        return boleto
