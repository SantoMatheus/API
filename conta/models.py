import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem


class StatusChoice(DjangoChoices):
    ativo = ChoiceItem('ativo')
    cancelado = ChoiceItem('cancelado')
    bloqueado = ChoiceItem('bloqueado')


class ContaCorrente(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    nome = models.CharField(max_length=55)
    cpf = models.CharField(max_length=11)
    saldo = models.FloatField(db_column='SALDO', default=0)
    agencia = models.CharField(max_length=6)
    num_conta = models.CharField(max_length=6)
    status = models.CharField(max_length=9, choices=StatusChoice, default='ativo')


class Saque(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conta_corrente = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE, related_name='conta_corrente_saque')
    valor = models.FloatField()


class Deposito(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conta_corrente = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE, related_name='conta_corrente_deposito')
    valor = models.FloatField()


class Transferencia(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conta_origem = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE,
                                     related_name='transferencias_origem')
    conta_destino = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE,
                                      related_name='transferencias_destino')
    valor = models.FloatField()
