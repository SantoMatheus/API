import uuid

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from transferencia.serializers import TransferenciaInputSerializer, TransferenciaOutputSerializer
from transferencia.service import transfer, consulta_transferencia


class TransferenciaView(APIView):
    def post(self, request: Request, agencia: str, num_conta: str):
        serializer = TransferenciaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agencia_destino = serializer.validated_data['agencia_destino']
        num_conta_destino = serializer.validated_data['num_conta_destino']
        valor = serializer.validated_data['valor']

        transferencia = transfer(agencia_origem=agencia, num_conta_origem=num_conta, agencia_destino=agencia_destino,
                                 num_conta_destino=num_conta_destino, valor=valor)
        output = TransferenciaOutputSerializer(instance=transferencia)

        return Response(data=output.data, status='202')


class ConsultaTransferenciaView(APIView):
    def get(self, id_transferencia: uuid.uuid4):
        transferencia = consulta_transferencia(id_transferencia=id_transferencia)

        output = TransferenciaOutputSerializer(instance=transferencia)

        return Response(data=output.data, status='200')
