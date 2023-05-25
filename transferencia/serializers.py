from rest_framework import serializers

from conta.serializers import ConsultarContaOutputSerializer
from transferencia.models import Transferencia


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
