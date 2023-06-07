from rest_framework import serializers

from conta.serializers import ConsultarContaOutputSerializer
from pix.models import TipoChavePixChoice, ChavePix


class CriarChavePixInputSerializer(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=TipoChavePixChoice)
    valor_chave = serializers.CharField(max_length=150, required=False)


class CriarChavePixOutputSerializer(serializers.ModelSerializer):
    conta_corrente = ConsultarContaOutputSerializer

    class Meta:
        model = ChavePix
        fields = ['id', 'valor_chave', 'tipo']
