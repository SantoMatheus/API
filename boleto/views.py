from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.serializers import (CriarBoletoInputSerializer, CriarBoletoOutputSerializer,
                                ConsultaBoletosOutputSerializer, ConsultaBoletosInputSerializer,
                                PagarBoletoInputSerializer)
from boleto.service import gerar_boleto, listar_boletos, pagar_boleto


class GerarBoletoView(APIView):
    def post(self, request: Request):
        serializer = CriarBoletoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        body = serializer.validated_data
        agencia = body['agencia']
        conta_corrente = body['conta_corrente']
        data_vencimento = body['data_vencimento']
        valor = body['valor']

        boleto = gerar_boleto(agencia=agencia, num_conta=conta_corrente, data_vencimento=data_vencimento, valor=valor)

        output = CriarBoletoOutputSerializer(instance=boleto)

        return Response(data=output.data, status=201)


class ConsultaBoletosView(APIView):
    def get(self, request: Request):
        serializer = ConsultaBoletosInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        num_conta = serializer.validated_data['num_conta']
        agencia = serializer.validated_data['agencia']

        boletos = listar_boletos(num_conta=num_conta, agencia=agencia)

        output = ConsultaBoletosOutputSerializer(instance=boletos, many=True)

        return Response(data=output.data, status=200)


class PagarBoletoView(APIView):
    def patch(self, request: Request, num_conta, agencia):
        serializer = PagarBoletoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_boleto = serializer.validated_data['id_boleto']
        try:
            boleto = pagar_boleto(agencia=agencia, num_conta=num_conta, id_boleto=id_boleto)

        except (BoletoPago, SaldoInsuficiente) as exc:
            return Response(status=400, data=exc.args[0])

        output = ConsultaBoletosOutputSerializer(instance=boleto)

        return Response(data=output.data, status=200)
