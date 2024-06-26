from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from extrato.serializers import ExtratoInputSerializer, ExtratoOutputSerializer
from extrato.use_cases.buscar_eventos_use_case import BuscarEventosUseCase


class BuscarEventosView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buscar_eventos_use_case = BuscarEventosUseCase()

    @swagger_auto_schema(
        query_serializer=ExtratoInputSerializer(),
        responses={
            status.HTTP_200_OK: ExtratoOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ExtratoInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')

        eventos = self.buscar_eventos_use_case.execute(agencia=agencia, conta_corrente=num_conta)

        return Response(data={'eventos': eventos}, status=status.HTTP_200_OK)
