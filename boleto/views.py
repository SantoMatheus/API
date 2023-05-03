from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from boleto.serializers import CriarBoletoInputSerializer, CriarBoletoOutputSerializer
from boleto.service import gerar_boleto


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
