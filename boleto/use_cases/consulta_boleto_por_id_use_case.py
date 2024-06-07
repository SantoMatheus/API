import uuid

from boleto.models import Boleto


class ConsultaBoletoPorIdUseCase:

    def execute(self, id_boleto: uuid.UUID):
        boleto = Boleto.objects.get(id=id_boleto)
        return boleto
