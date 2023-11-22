from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.serializers import (CriarBoletoInputSerializer, CriarBoletoOutputSerializer,
                                ConsultaBoletosOutputSerializer, ConsultaBoletosInputSerializer,
                                PagarBoletoInputSerializer)

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


class ConsultaBoletosView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gerar_boleto_use_case = GerarBoletoUseCase()
        self.listar_boletos_use_case = ListarBoletoUseCase()

    def get(self, request: Request):
        serializer = ConsultaBoletosInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        num_conta = serializer.validated_data.get('num_conta')
        agencia = serializer.validated_data.get('agencia')
        pago = serializer.validated_data.get('pago')
        id_boleto = serializer.validated_data.get('id_boleto')

        boletos = self.listar_boletos_use_case.execute(num_conta=num_conta, agencia=agencia, pago=pago,
                                                       id_boleto=id_boleto)

        output = ConsultaBoletosOutputSerializer(instance=boletos, many=True)

        return Response(data=output.data, status=200)


class PagarBoletoView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagar_boleto_use_case = PagarBoletoUseCase()

    def patch(self, request: Request, num_conta, agencia):
        serializer = PagarBoletoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_boleto = serializer.validated_data['id_boleto']
        try:
            boleto = self.pagar_boleto_use_case.execute(agencia=agencia, num_conta=num_conta, id_boleto=id_boleto)

        except (BoletoPago, SaldoInsuficiente) as exc:
            return Response(status=400, data=exc.args[0])

        output = ConsultaBoletosOutputSerializer(instance=boleto)

        return Response(data=output.data, status=200)
