from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.serializers import (CriarBoletoInputSerializer, CriarBoletoOutputSerializer,
                                ListarBoletosOutputSerializer, ListarBoletosInputSerializer,
                                ConsultaBoletoPorIdInputSerializer)
from boleto.use_cases.cancelar_boleto_use_case import CancelarBoletoUseCase
from boleto.use_cases.consulta_boleto_por_id_use_case import ConsultaBoletoPorIdUseCase
from boleto.use_cases.gerar_boleto_use_case import GerarBoletoUseCase
from boleto.use_cases.listar_boleto_use_case import ListarBoletoUseCase
from boleto.use_cases.pagar_boleto_use_case import PagarBoletoUseCase


class GerarBoletoView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gerar_boleto_use_case = GerarBoletoUseCase()

    @swagger_auto_schema(
        request_body=CriarBoletoInputSerializer(),
        responses={
            status.HTTP_201_CREATED: CriarBoletoOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def post(self, request: Request):
        serializer = CriarBoletoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        body = serializer.validated_data
        agencia = body['agencia']
        conta_corrente = body['conta_corrente']
        data_vencimento = body['data_vencimento']
        valor = body['valor']

        boleto = self.gerar_boleto_use_case.execute(agencia=agencia, num_conta=conta_corrente,
                                                    data_vencimento=data_vencimento, valor=valor)

        output = CriarBoletoOutputSerializer(instance=boleto)

        return Response(data=output.data, status=201)


class ListarBoletosView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listar_boletos_use_case = ListarBoletoUseCase()

    @swagger_auto_schema(
        query_serializer=ListarBoletosInputSerializer(),
        responses={
            status.HTTP_201_CREATED: ListarBoletosOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ListarBoletosInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_conta = serializer.validated_data.get('id_conta')
        agencia = serializer.validated_data.get('agencia')
        status_boleto = serializer.validated_data.get('status')
        id_boleto = serializer.validated_data.get('id_boleto')

        boletos = self.listar_boletos_use_case.execute(id_conta=id_conta, agencia=agencia,
                                                       status=status_boleto,
                                                       id_boleto=id_boleto)

        output = ListarBoletosOutputSerializer(instance=boletos, many=True)

        return Response(data=output.data, status=200)


class PagarBoletoView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagar_boleto_use_case = PagarBoletoUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultaBoletoPorIdInputSerializer(),
        responses={
            status.HTTP_201_CREATED: ListarBoletosOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request, num_conta_sacado: str, agencia_sacado: str):
        serializer = ConsultaBoletoPorIdInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_boleto = serializer.validated_data['id_boleto']

        try:
            boleto = self.pagar_boleto_use_case.execute(id_boleto=id_boleto, num_conta_sacado=num_conta_sacado,
                                                        agencia_sacado=agencia_sacado)

        except (BoletoPago, SaldoInsuficiente) as exc:
            return Response(status=400, data=exc.args[0])

        output = ListarBoletosOutputSerializer(instance=boleto)

        return Response(data=output.data, status=200)


class CancelarBoletoView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cancelar_boleto_use_case = CancelarBoletoUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultaBoletoPorIdInputSerializer(),
        responses={
            status.HTTP_201_CREATED: CriarBoletoOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def delete(self, request: Request):
        serializer = ConsultaBoletoPorIdInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_boleto = serializer.validated_data['id_boleto']

        try:
            boleto = self.cancelar_boleto_use_case.execute(id_boleto=id_boleto)

        except BoletoPago as exc:
            return Response(status=400, data=exc.args[0])

        output = CriarBoletoOutputSerializer(instance=boleto)

        return Response(data=output.data, status=200)


class ConsultaBoletoPorIdView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.consulta_boleto_por_id_use_case = ConsultaBoletoPorIdUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultaBoletoPorIdInputSerializer(),
        responses={
            status.HTTP_201_CREATED: CriarBoletoOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultaBoletoPorIdInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_boleto = serializer.validated_data['id_boleto']

        boleto = self.consulta_boleto_por_id_use_case.execute(id_boleto=id_boleto)

        output = CriarBoletoOutputSerializer(instance=boleto)

        return Response(data=output.data, status=200)
