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


class Boleto(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    conta_corrente = models.ForeignKey(ContaCorrente, db_column='CONTA_CORRENT_ID', on_delete=models.CASCADE)
    valor = models.FloatField()
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)
