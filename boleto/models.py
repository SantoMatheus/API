import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel
from conta.models import ContaCorrente


class Boleto(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    conta_corrente = models.ForeignKey(ContaCorrente, db_column='CONTA_CORRENT_ID', on_delete=models.CASCADE)
    valor = models.FloatField()
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)

