from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from conta.factories import ContaCorrenteFactories
from conta.serializers import CriarContaSerializer, ContaCorrenteSerializer, ConsultarContaOutputSerializer, \
    DepositoInputSerializer, SaqueInputSerializer, TransferenciaInputSerializer, \
    MulticontaInputSerializer, ConsultarContaInputSerializer
from conta.service import criar_conta, consultar_conta, aumentar_saldo, diminuir_saldo, multiconta


class CriarContaView(APIView):
    def post(self, request):
        serializer = CriarContaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        body = serializer.validated_data
        nome = body['nome']
        cpf = body['cpf']
        conta = criar_conta(nome=nome, cpf=cpf)

        output = ContaCorrenteSerializer(instance=conta)

        return Response(data=output.data, status='201')


class ConsultarContaView(APIView):
    def get(self, request: Request):
        serializer = ConsultarContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')
        cpf = serializer.validated_data.get('cpf')
        id_conta = serializer.validated_data.get('id_conta')

        conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta, cpf=cpf, id_conta=id_conta)

        output = ConsultarContaOutputSerializer(instance=conta_corrente, many=True)

        return Response(data=output.data, status='200')


class DepositoView(APIView):
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = DepositoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_deposito = serializer.validated_data['valor_deposito']

        conta_atualizada = aumentar_saldo(agencia=agencia, num_conta=num_conta, valor_deposito=valor_deposito)
        output = ConsultarContaOutputSerializer(instance=conta_atualizada)

        return Response(data=output.data, status='202')


class SaqueView(APIView):
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = SaqueInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_saque = serializer.validated_data['valor_saque']

        conta_atualizada = diminuir_saldo(agencia=agencia, num_conta=num_conta, valor_saque=valor_saque)
        output = ConsultarContaOutputSerializer(instance=conta_atualizada)

        return Response(data=output.data, status='202')


class MulticontaView(APIView):
    def post(self, request: Request):
        serializer = MulticontaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        body = serializer.validated_data
        agencia = body['agencia']
        numero_conta_origem = body['conta_origem']

        conta_corrente = multiconta(agencia=agencia, num_conta=numero_conta_origem)

        output = ConsultarContaOutputSerializer(instance=conta_corrente)

        return Response(data=output.data, status=200)


class IdealConsultaContaView(APIView):
    get_output_serializer = ConsultarContaOutputSerializer
    get_sucess_status = 200

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._consultar_conta_use_case = ContaCorrenteFactories.make_consultar_conta_use_case()

    def get(self, request, agencia, conta):
        conta_corrente = self._consultar_conta_use_case.execute(agencia=agencia, conta=conta)

        output = self.get_output_serializer(instance=conta_corrente)
        return Response(data=output.data, status=self.get_sucess_status)
