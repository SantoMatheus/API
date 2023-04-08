from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from conta.serializers import CriarContaSerializer, ContaCorrenteSerializer, ConsultarContaSerializer, \
    ConsultarContaOutputSerializer
from conta.service import criar_conta, consultar_conta


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
        data_dict = {'agencia': agencia, 'num_conta': num_conta}
        serializer = ConsultarContaSerializer(data=data_dict)
        serializer.is_valid(raise_exception=True)

        conta = consultar_conta(agencia=agencia, num_conta=num_conta)

        output = ConsultarContaOutputSerializer(instance=conta)

        return Response(data=output.data, status='200')





