from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.views import APIView

from pix.exceptions.valor_chave_requerido import ValorChaveRequerido
from pix.serializers import CriarChavePixInputSerializer, CriarChavePixOutputSerializer
from pix.use_cases.criar_chave_pix_use_case import CriarChavePixUseCase


class CriarChavePixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chave_pix_use_case = CriarChavePixUseCase()

    def post(self, request: Request, agencia: str, num_conta: str):
        serializer = CriarChavePixInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tipo = serializer.validated_data['tipo']
        valor_chave = serializer.validated_data.get('valor_chave')

        try:
            chave_pix = self.chave_pix_use_case.execute(agencia=agencia, num_conta=num_conta, tipo=tipo,
                                                        valor_chave=valor_chave)
        except ValorChaveRequerido as exc:
            return Response(data=exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        output = CriarChavePixOutputSerializer(instance=chave_pix)

        return Response(data=output.data, status=status.HTTP_201_CREATED)






