import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem

from conta.models import ContaCorrente
from common_modules.definir_vencimento_cobranca_use_case import DefinirVencimentoCobrancaUseCase


class TipoChavePixChoice(DjangoChoices):
    CELULAR = ChoiceItem('CELULAR')
    CNPJ = ChoiceItem('CNPJ')
    CPF = ChoiceItem('CPF')
    EMAIL = ChoiceItem('EMAIL')
    EVP = ChoiceItem('EVP')


class ChavePix(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    conta_corrente = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE)
    valor_chave = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50, choices=TipoChavePixChoice)
    esta_ativa = models.BooleanField(default=True)


class CobrancaStatusChoice(DjangoChoices):
    aguardando_pagamento = ChoiceItem('aguardando_pagamento')
    pago = ChoiceItem('pago')
    cancelado = ChoiceItem('cancelado')
    vencido = ChoiceItem('vencido')
    pagamento_devolvido = ChoiceItem('pagamento_devolvido')


class TransferenciaPix(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    conta_origem = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE, related_name='conta_corrente_origem')
    conta_destino = models.ForeignKey(ChavePix, on_delete=models.CASCADE, related_name='chave_pix_destino')
    status = models.CharField(max_length=20, choices=CobrancaStatusChoice, default='aguardando_pagamento')
    valido_ate = models.DateTimeField(default=DefinirVencimentoCobrancaUseCase.execute)
    valor = models.FloatField()


class PagamentoPix(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    cobranca_pix = models.ForeignKey(TransferenciaPix, on_delete=models.CASCADE, related_name='cobranca_id')


class DevolucaoPix(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    pagamento = models.ForeignKey(PagamentoPix, on_delete=models.CASCADE, related_name='pagamento_id')
    valor_a_devolver = models.FloatField()

