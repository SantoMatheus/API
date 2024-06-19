from rest_framework import serializers

from boleto.models import Boleto, PagamentoBoleto


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
    id_conta = serializers.CharField(required=False)
    agencia = serializers.CharField(required=False)
    num_conta = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    id_boleto = serializers.UUIDField(required=False)
    valor = serializers.FloatField(required=False)
    data_vencimento = serializers.DateTimeField(required=False)


class ConsultaBoletoPorIdInputSerializer(serializers.Serializer):
    id_boleto = serializers.UUIDField()


class PagamentoBoletoOutputSerializer(serializers.ModelSerializer):
    boleto = CriarBoletoOutputSerializer()

    class Meta:
        model = PagamentoBoleto
        fields = '__all__'

