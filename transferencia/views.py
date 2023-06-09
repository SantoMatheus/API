import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transferencia.serializers import TransferenciaInputSerializer, TransferenciaOutputSerializer
from transferencia.service import transfer, consulta_transferencia, listar_transferencias


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
    def get(self, request, agencia_origem: str, num_conta_origem: str, id_transferencia: uuid.UUID):

        try:
            transferencia = consulta_transferencia(agencia=agencia_origem, num_conta_origem=num_conta_origem,
                                                   id_transferencia=id_transferencia)

        except ObjectDoesNotExist:
            return Response(status='404')

        output = TransferenciaOutputSerializer(instance=transferencia)

        return Response(data=output.data, status='200')


class ListarTransferenciaView(APIView):
    def get(self, request, num_conta_origem: str, agencia_origem: str):
        transferencia = listar_transferencias(agencia_origem=agencia_origem, num_conta_origem=num_conta_origem)

        output = TransferenciaOutputSerializer(instance=transferencia, many=True)

        return Response(data=output.data, status='200')
