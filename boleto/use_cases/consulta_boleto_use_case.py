import uuid

from boleto.models import Boleto


class ConsultarBoletoUseCase:

    def execute(self, id_boleto: uuid.UUID):
        boleto = Boleto.objects.get(id_boleto=id_boleto)
        return boleto
