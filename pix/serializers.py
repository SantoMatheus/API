from rest_framework import serializers

from conta.models import ContaCorrente
from conta.serializers import ConsultarContaOutputSerializer
from pix.models import TipoChavePixChoice, ChavePix, TransferenciaPix, PagamentoPix


class DadosContaCorrenteOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaCorrente
        fields = ['nome', 'cpf', 'num_conta']


class CriarChavePixInputSerializer(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=TipoChavePixChoice)
    valor_chave = serializers.CharField(max_length=150, required=False)


class CriarChavePixOutputSerializer(serializers.ModelSerializer):
    conta_corrente = DadosContaCorrenteOutputSerializer()

    class Meta:
        model = ChavePix
        fields = '__all__'


class ConsultarChavePixPorContaInputSerializer(serializers.Serializer):
    num_conta = serializers.CharField(max_length=10)
    agencia = serializers.CharField(max_length=4)


class ConsultarChavePixPeloHashInputSerializer(serializers.Serializer):
    valor_chave = serializers.CharField(max_length=100)


class CriarCobrancaPixInputSerializer(serializers.Serializer):
    chave_pix_origem = serializers.CharField(max_length=150, min_length=11)
    chave_pix_destino = serializers.CharField(max_length=150, min_length=11)
    valor_transferencia = serializers.FloatField()
    validade = serializers.IntegerField()


class CriarCobrancaPixOutputSerializer(serializers.ModelSerializer):
    conta_destino = CriarChavePixOutputSerializer()

    class Meta:
        model = TransferenciaPix
        fields = '__all__'


class PagarPixInputSerializer(serializers.Serializer):
    id_cobranca = serializers.CharField(max_length=50)


class PagamentoPixOutputSerializer(serializers.ModelSerializer):
    cobranca_pix = CriarCobrancaPixOutputSerializer

    class Meta:
        model = PagamentoPix
        field = '__all__'
