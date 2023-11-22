from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from conta.exceptions.saldo_insuficiente import SaldoInsuficiente
from conta.serializers import CriarContaSerializer, ContaCorrenteSerializer, ConsultarContaOutputSerializer, \
    DepositoInputSerializer, SaqueInputSerializer, \
    MulticontaInputSerializer, ConsultarContaInputSerializer
from conta.use_cases.consultar_conta_use_case import ListarContaUseCase
from conta.use_cases.criar_conta_use_case import CriarContaUseCase
from conta.use_cases.deposito_use_case import DepositoUseCase
from conta.use_cases.multiconta_use_case import MulticontaUseCase
from conta.use_cases.saque_use_case import SaqueUseCase


class CriarContaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.criar_conta_use_case = CriarContaUseCase()

    @extend_schema(
        request=CriarContaSerializer(),
        responses={status.HTTP_201_CREATED: ContaCorrenteSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'},
    )
    def post(self, request):
        serializer = CriarContaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nome = serializer.validated_data['nome']
        cpf = serializer.validated_data['cpf']

        conta = self.criar_conta_use_case.execute(nome=nome, cpf=cpf)

        output = ContaCorrenteSerializer(instance=conta)
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class ListarContaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listar_conta_use_case = ListarContaUseCase()

    @extend_schema(
        request=CriarContaSerializer(),
        responses={status.HTTP_201_CREATED: ContaCorrenteSerializer(),
                   status.HTTP_400_BAD_REQUEST: 'Bad request.'},
    )
    def get(self, request: Request):
        serializer = ConsultarContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')
        id_conta = serializer.validated_data.get('id_conta')
        cpf = serializer.validated_data.get('cpf')

        conta_corrente = self.listar_conta_use_case.execute(agencia=agencia, num_conta=num_conta, cpf=cpf,
                                                            id_conta=id_conta)

        output = ConsultarContaOutputSerializer(instance=conta_corrente, many=True)
        return Response(data=output.data, status='200')


class DepositoView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deposito_use_case = DepositoUseCase()

    @swagger_auto_schema(
        request_body=DepositoInputSerializer(),
        responses={
            status.HTTP_201_CREATED: ConsultarContaOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = DepositoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_deposito = serializer.validated_data['valor_deposito']

        try:
            conta_atualizada = self.deposito_use_case.execute(agencia=agencia, num_conta=num_conta,
                                                              valor_deposito=valor_deposito)
        except SaldoInsuficiente as exc:
            return Response(data=exc.args[0], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        output = ConsultarContaOutputSerializer(instance=conta_atualizada)
        return Response(data=output.data, status='202')


class SaqueView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.saque_use_case = SaqueUseCase()

    @swagger_auto_schema(
        request_body=SaqueInputSerializer(),
        responses={
            status.HTTP_201_CREATED: ConsultarContaOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = SaqueInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_saque = serializer.validated_data['valor_saque']

        try:
            conta_atualizada = self.saque_use_case.execute(agencia=agencia, num_conta=num_conta,
                                                           valor_saque=valor_saque)
        except SaldoInsuficiente as exc:
            return Response(data=exc.args[0], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        output = ConsultarContaOutputSerializer(instance=conta_atualizada)
        return Response(data=output.data, status='202')


class MulticontaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.multiconta_use_case = MulticontaUseCase()

    @swagger_auto_schema(
        request_body=MulticontaInputSerializer(),
        responses={
            status.HTTP_201_CREATED: ConsultarContaOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def post(self, request: Request):
        serializer = MulticontaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data['agencia']
        numero_conta_origem = serializer.validated_data['conta_origem']

        conta_corrente = self.multiconta_use_case.execute(agencia=agencia, num_conta=numero_conta_origem)

        output = ConsultarContaOutputSerializer(instance=conta_corrente)
        return Response(data=output.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
