from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from conta.serializers import CriarContaSerializer, ContaCorrenteSerializer
from conta.service import criar_conta


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

    def get(self, request):
        return Response(data={'resposta': 'Não implementado'}, status='200')

