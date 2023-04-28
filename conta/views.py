from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from conta.serializers import CriarContaSerializer, ContaCorrenteSerializer, ConsultarContaSerializer, \
    ConsultarContaOutputSerializer, DepositoInputSerializer, SaqueInputSerializer, TransferenciaInputSerializer, \
    MulticontaInputSerializer
from conta.service import criar_conta, consultar_conta, aumentar_saldo, diminuir_saldo, transferir_saldo, multiconta


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


class SaqueView(APIView):
    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = SaqueInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_saque = serializer.validated_data['valor_saque']

        conta_atualizada = diminuir_saldo(agencia=agencia, num_conta=num_conta, valor_saque=valor_saque)
        output = ConsultarContaOutputSerializer(instance=conta_atualizada)

        return Response(data=output.data, status='202')


class TransferenciaView(APIView):
    def post(self, request: Request):
        serializer = TransferenciaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        body = serializer.validated_data
        agencia_origem = body['agencia_origem']
        conta_origem = body['conta_origem']
        agencia_destino = body['agencia_destino']
        conta_destino = body['conta_destino']
        valor = body['valor']

        conta_corrente = transferir_saldo(agencia_origem=agencia_origem,
                                          conta_origem=conta_origem,
                                          valor=valor,
                                          agencia_destino=agencia_destino,
                                          conta_destino=conta_destino)

        output = ConsultarContaOutputSerializer(instance=conta_corrente)

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