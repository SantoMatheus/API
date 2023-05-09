from rest_framework import serializers

from boleto.models import Boleto
from conta.serializers import ConsultarContaOutputSerializer


class CriarBoletoInputSerializer(serializers.Serializer):
    conta_corrente = serializers.CharField(max_length=6)
    agencia = serializers.CharField(max_length=6)
    data_vencimento = serializers.DateField()
    valor = serializers.FloatField(required=True)


class CriarBoletoOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleto
        fields = '__all__'


class ConsultaBoletosInputSerializer(serializers.Serializer):
    num_conta = serializers.CharField(max_length=6)
    agencia = serializers.CharField(max_length=6)


class ConsultaBoletosOutputSerializer(serializers.ModelSerializer):
    conta_corrente = ConsultarContaOutputSerializer()

    class Meta:
        model = Boleto
        fields = '__all__'


class PagarBoletoInputSerializer(serializers.Serializer):
    id_boleto = serializers.UUIDField()