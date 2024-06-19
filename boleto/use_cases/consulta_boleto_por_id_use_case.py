import uuid

from boleto.models import Boleto


class ConsultaBoletoPorIdUseCase:

    def execute(self, id_boleto: uuid.UUID):
        return Boleto.objects.get(id=id_boleto)

