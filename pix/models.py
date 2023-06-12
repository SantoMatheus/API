import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem

from conta.models import ContaCorrente


class TipoChavePixChoice(DjangoChoices):
    CELULAR = ChoiceItem('CELULAR')
    CNPJ = ChoiceItem('CNPJ')
    CPF = ChoiceItem('CPF')
    EMAIL = ChoiceItem('EMAIL')
    EVP = ChoiceItem('EVP')


class ChavePix(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conta_corrente = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE)
    valor_chave = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50, choices=TipoChavePixChoice)


