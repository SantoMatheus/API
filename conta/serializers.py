from rest_framework import serializers

from conta.models import ContaCorrente


class CriarContaSerializer(serializers.Serializer):
    nome = serializers.CharField(required=True, max_length=55)
    cpf = serializers.CharField(required=True, max_length=11, min_length=11)


class ContaCorrenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaCorrente
        exclude = ['created', 'modified']
