import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel


class ContaCorrente(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    nome = models.CharField(max_length=55)
    cpf = models.CharField(max_length=11)
    saldo = models.FloatField(db_column='SALDO', default=0)
    agencia = models.CharField(max_length=6)
    num_conta = models.CharField(max_length=6)

    objects = models.Manager()

