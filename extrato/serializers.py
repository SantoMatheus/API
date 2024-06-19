from rest_framework import serializers

from boleto.serializers import PagamentoBoletoOutputSerializer
from conta.serializers import DepositoOutputSerializer
from pix.serializers import PagamentoPixOutputSerializer
from transferencia.serializers import TransferenciaOutputSerializer


class ExtratoInputSerializer(serializers.Serializer):
    agencia = serializers.CharField(max_length=4)
    num_conta = serializers.CharField(max_length=10)


class ExtratoOutputSerializer(serializers.ModelSerializer):
    boleto = PagamentoBoletoOutputSerializer
    pix = PagamentoPixOutputSerializer
    devolucao_pix = PagamentoPixOutputSerializer
    saque = DepositoOutputSerializer
    deposito = DepositoOutputSerializer
    transferencia = TransferenciaOutputSerializer
