import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel

from conta.models import ContaCorrente


class Transferencia(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conta_origem = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE,
                                     related_name='transferencias_como_origem')
    conta_destino = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE,
                                      related_name='transferencias_como_destino')
    valor = models.FloatField(default=0)
