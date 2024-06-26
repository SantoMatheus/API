import uuid

from rest_framework.exceptions import ValidationError

from boleto.models import Boleto


class ConsultaBoletoPorIdUseCase:
    def execute(self, id_boleto: uuid.UUID):
        if not id_boleto:
            raise ValidationError('Informar id do boleto.')

        return Boleto.objects.get(id=id_boleto)

