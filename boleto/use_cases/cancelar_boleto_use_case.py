import uuid

from boleto.use_cases.consulta_boleto_por_id_use_case import ConsultaBoletoPorIdUseCase


class CancelarBoletoUseCase:

    def __init__(self):
        self.consulta_boleto_use_case = ConsultaBoletoPorIdUseCase()

    def execute(self, id_boleto: uuid.UUID):
        boleto = self.consulta_boleto_use_case.execute(id_boleto=id_boleto)
        boleto.status = "Cancelado"
        boleto.save()
        boleto.conta_corrente.save()
        return boleto
