from rest_framework import serializers

from boleto.serializers import PagamentoBoletoOutputSerializer
from conta.models import ContaCorrente
from conta.serializers import DepositoOutputSerializer, TransferenciaOutputSerializer, SaqueOutputSerializer
from pix.serializers import PagamentoPixOutputSerializer, DevolucaoPixOutputSerializer


class ExtratoInputSerializer(serializers.Serializer):
    agencia = serializers.CharField(max_length=4)
    num_conta = serializers.CharField(max_length=10)


class ExtratoOutputSerializer(serializers.ModelSerializer):
    pagamento_boleto = PagamentoBoletoOutputSerializer()
    pagamento_pix = PagamentoPixOutputSerializer()
    devolucao_pix = DevolucaoPixOutputSerializer()
    saque = SaqueOutputSerializer()
    deposito = DepositoOutputSerializer()
    transferencia = TransferenciaOutputSerializer()

    class Meta:
        model = ContaCorrente
        fields = '__all__'
