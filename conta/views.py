from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from conta.serializers import CriarContaInputSerializer, CriarContaCorrenteOutputSerializer, \
    ConsultarContaOutputSerializer, DepositoInputSerializer, SaqueInputSerializer, MulticontaInputSerializer, \
    ConsultarContaInputSerializer, TransferenciaInputSerializer, TransferenciaOutputSerializer, \
    ListarTransferenciaInputSerializer, DepositoOutputSerializer, SaqueOutputSerializer
from conta.use_cases.criar_conta_use_case import CriarContaUseCase
from conta.use_cases.criar_transferencia_use_case import CriarTransferenciaUseCase
from conta.use_cases.deposito_use_case import DepositoUseCase
from conta.use_cases.excluir_conta_use_case import CancelarContaUseCase
from conta.use_cases.listar_conta_use_case import ListarContaUseCase
from conta.use_cases.listar_transferencia_use_case import ListarTransferenciaUseCase
from conta.use_cases.multiconta_use_case import MulticontaUseCase
from conta.use_cases.saque_use_case import SaqueUseCase


class CriarContaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.criar_conta_use_case = CriarContaUseCase()

    @swagger_auto_schema(
        request_body=CriarContaInputSerializer(),
        responses={status.HTTP_201_CREATED: CriarContaCorrenteOutputSerializer(),
                   status.HTTP_400_BAD_REQUEST: 'Bad request.'},
    )
    def post(self, request):
        serializer = CriarContaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nome = serializer.validated_data['nome']
        cpf = serializer.validated_data['cpf']

        conta = self.criar_conta_use_case.execute(nome=nome, cpf=cpf)

        output = CriarContaCorrenteOutputSerializer(instance=conta)
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class ListarContaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listar_conta_use_case = ListarContaUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarContaInputSerializer(),
        responses={status.HTTP_200_OK: CriarContaCorrenteOutputSerializer(),
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
        return Response(data=output.data, status=status.HTTP_200_OK)


class DepositoView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deposito_use_case = DepositoUseCase()

    @swagger_auto_schema(
        request_body=DepositoInputSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: DepositoOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = DepositoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_deposito = serializer.validated_data['valor_deposito']

        conta_atualizada = self.deposito_use_case.execute(agencia=agencia, num_conta=num_conta,
                                                          valor_deposito=valor_deposito)

        output = DepositoOutputSerializer(instance=conta_atualizada)
        return Response(data=output.data, status=status.HTTP_202_ACCEPTED)


class SaqueView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.saque_use_case = SaqueUseCase()

    @swagger_auto_schema(
        request_body=SaqueInputSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: SaqueOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = SaqueInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_saque = serializer.validated_data['valor_saque']

        conta_atualizada = self.saque_use_case.execute(agencia=agencia, num_conta=num_conta,
                                                       valor_saque=valor_saque)

        output = SaqueOutputSerializer(instance=conta_atualizada)
        return Response(data=output.data, status=status.HTTP_202_ACCEPTED)


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
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class TransferenciaView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.criar_transferencia_use_case = CriarTransferenciaUseCase()

    @swagger_auto_schema(
        request_body=TransferenciaInputSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: TransferenciaOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def post(self, request: Request, agencia: str, num_conta: str):
        serializer = TransferenciaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agencia_destino = serializer.validated_data['agencia_destino']
        num_conta_destino = serializer.validated_data['num_conta_destino']
        valor = serializer.validated_data['valor']

        transferencia = self.criar_transferencia_use_case.execute(agencia_origem=agencia, num_conta_origem=num_conta,
                                                                  agencia_destino=agencia_destino,
                                                                  num_conta_destino=num_conta_destino, valor=valor)
        output = TransferenciaOutputSerializer(instance=transferencia)

        return Response(data=output.data, status=status.HTTP_202_ACCEPTED)


class ListarTransferenciaView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consultar_transferencia_use_case = ListarTransferenciaUseCase()

    @swagger_auto_schema(
        query_serializer=ListarTransferenciaInputSerializer(),
        responses={
            status.HTTP_200_OK: TransferenciaOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ListarTransferenciaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia_origem = serializer.validated_data['agencia_origem']
        num_conta_origem = serializer.validated_data['num_conta_origem']
        agencia_destino = serializer.validated_data['agencia_destino']
        num_conta_destino = serializer.validated_data['num_conta_destino']
        id_transferencia = serializer.validated_data['id_transferencia']
        valor = serializer.validated_data['valor']

        transferencia = self.consultar_transferencia_use_case.execute(agencia_origem=agencia_origem,
                                                                      num_conta_origem=num_conta_origem,
                                                                      agencia_destino=agencia_destino,
                                                                      num_conta_destino=num_conta_destino,
                                                                      id_transferencia=id_transferencia, valor=valor)

        output = TransferenciaOutputSerializer(instance=transferencia, many=True)

        return Response(data=output.data, status=status.HTTP_200_OK)


class CancelarContaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cancelar_conta_use_case = CancelarContaUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarContaInputSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: ConsultarContaOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def delete(self, request: Request):
        serializer = ConsultarContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia', None)
        num_conta = serializer.validated_data.get('num_conta', None)
        cpf = serializer.validated_data.get('cpf', None)
        id_conta = serializer.validated_data.get('id_conta', None)

        conta = self.cancelar_conta_use_case.execute(agencia=agencia, num_conta=num_conta, cpf=cpf, id_conta=id_conta)

        output = ConsultarContaOutputSerializer(instance=conta)

        return Response(data=output.data, status=status.HTTP_202_ACCEPTED)
