from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from conta.serializers import CriarContaSerializer, ContaCorrenteSerializer, ConsultarContaSerializer, \
    ConsultarContaOutputSerializer, DepositoInputSerializer
from conta.service import criar_conta, consultar_conta, aumentar_saldo


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
    def get(self, request, agencia, num_conta):
        conta = consultar_conta(agencia=agencia, num_conta=num_conta)

        output = ConsultarContaOutputSerializer(instance=conta)

        return Response(data=output.data, status='200')

class DepositoView(APIView):
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = DepositoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_deposito = serializer.validated_data['valor_deposito']

        conta_atualizada = aumentar_saldo(agencia=agencia, num_conta=num_conta, valor_deposito=valor_deposito)
        output = ConsultarContaOutputSerializer(instance=conta_atualizada)

        return Response(data=output.data, status='202')

