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


class ListarBoletosInputSerializer(serializers.Serializer):
    num_conta = serializers.CharField(max_length=6, required=False)
    pago = serializers.BooleanField(required=False)
    id_boleto = serializers.UUIDField(required=False)


class ListarBoletosOutputSerializer(serializers.ModelSerializer):
    conta_corrente = ConsultarContaOutputSerializer()

    class Meta:
        model = Boleto
        fields = '__all__'


class ConsultarBoletoInputSerializer(serializers.Serializer):
    id_boleto = serializers.UUIDField()

