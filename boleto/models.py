import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem

from common_modules.definir_vencimento_cobranca_use_case import DefinirVencimentoCobrancaUseCase
from conta.models import ContaCorrente


class StatusBoletoChoice(DjangoChoices):
    pagamento_pendente = ChoiceItem('pagamento_pendente')
    pago = ChoiceItem('pago')
    vencido = ChoiceItem('vencido')
    cancelado = ChoiceItem('cancelado')


class Boleto(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    conta_corrente = models.ForeignKey(ContaCorrente, db_column='CONTA_CORRENT_ID', on_delete=models.CASCADE)
    valor = models.FloatField()
    data_vencimento = models.DateField(default=DefinirVencimentoCobrancaUseCase.execute)
    status = models.CharField(max_length=20, choices=StatusBoletoChoice, default='pagamento_pendente')


class PagamentoBoleto(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    boleto = models.ForeignKey(Boleto, on_delete=models.CASCADE, related_name='boleto_cobranca')
    conta_sacado = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE, related_name='conta_sacado')


