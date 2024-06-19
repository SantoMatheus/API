from rest_framework import serializers
from conta.models import ContaCorrente, Saque, Transferencia, Deposito


class CriarContaInputSerializer(serializers.Serializer):
    nome = serializers.CharField(required=True, max_length=55)
    cpf = serializers.CharField(required=True, max_length=11, min_length=11)


class CriarContaCorrenteOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaCorrente
        exclude = ['created', 'modified']


class ConsultarContaInputSerializer(serializers.Serializer):
    agencia = serializers.CharField(max_length=6, required=False, allow_null=True)
    num_conta = serializers.CharField(max_length=6, required=False, allow_null=True)
    id_conta = serializers.UUIDField(required=False, allow_null=True)
    cpf = serializers.CharField(max_length=11, required=False, allow_null=True)


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

class SaqueOutputSerializer(serializers.ModelSerializer):
    conta_corrente = ConsultarContaOutputSerializer()

    class Meta:
        model = Saque
        fields = '__all__'


class DepositoOutputSerializer(serializers.ModelSerializer):
    conta_corrente = ConsultarContaOutputSerializer()

    class Meta:
        model = Deposito
        fields = '__all__'


class TransferenciaInputSerializer(serializers.Serializer):
    agencia_destino = serializers.CharField(max_length=6, required=True)
    num_conta_destino = serializers.CharField(max_length=6, required=True)
    valor = serializers.FloatField(required=True)


class TransferenciaOutputSerializer(serializers.ModelSerializer):
    conta_origem = ConsultarContaOutputSerializer()
    conta_destino = ConsultarContaOutputSerializer()

    class Meta:
        model = Transferencia
        fields = '__all__'


class ListarTransferenciaInputSerializer(serializers.Serializer):
    agencia_origem = serializers.CharField(required=False)
    num_conta_origem = serializers.CharField(required=False)
    agencia_destino = serializers.CharField(required=False)
    num_conta_destino = serializers.CharField(required=False)
    id_transferencia = serializers.UUIDField(required=False)
    valor = serializers.FloatField(required=False)
