from rest_framework import serializers

from conta.models import ContaCorrente


class CriarContaSerializer(serializers.Serializer):
    nome = serializers.CharField(required=True, max_length=55)
    cpf = serializers.CharField(required=True, max_length=11, min_length=11)


class ContaCorrenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaCorrente
        exclude = ['created', 'modified']


class ConsultarContaSerializer(serializers.Serializer):
    agencia = serializers.CharField(max_length=6)
    num_conta = serializers.CharField(max_length=6)


class ConsultarContaOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaCorrente
        fields = '__all__'


class DepositoInputSerializer(serializers.Serializer):
    valor_deposito = serializers.FloatField(required=True)


class SaqueInputSerializer(serializers.Serializer):
    valor_saque = serializers.FloatField(required=True)


class TransferenciaInputSerializer(serializers.Serializer):
    agencia_origem = serializers.CharField(max_length=6)
    conta_origem = serializers.CharField(max_length=6)
    agencia_destino = serializers.CharField(max_length=6)
    conta_destino = serializers.CharField(max_length=6)
    valor = serializers.FloatField(required=True)


class MulticontaInputSerializer(serializers.Serializer):
    agencia = serializers.CharField(max_length=6)
    conta_origem = serializers.CharField(max_length=6)
