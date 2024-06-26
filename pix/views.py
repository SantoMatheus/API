from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pix.exceptions.valor_chave_requerido import ValorChaveRequerido
from pix.serializers import CriarChavePixInputSerializer, CriarChavePixOutputSerializer, \
    ConsultarChavePixPorContaInputSerializer, ConsultarChavePixPeloHashInputSerializer, \
    CriarCobrancaPixOutputSerializer, CriarCobrancaPixInputSerializer, \
    PagarPixInputSerializer, PagamentoPixOutputSerializer, DevolucaoPixInputSerializer, DevolucaoPixOutputSerializer
from pix.use_cases.buscar_cobranca_use_case import BuscarCobrancaPixUseCase
from pix.use_cases.buscar_pagamento_pix_use_case import BuscarPagamentoPixUseCase
from pix.use_cases.consultar_chave_pix_por_conta_use_case import ConsultarChavePixPorContaUseCase
from pix.use_cases.consultar_chave_pix_por_hash_use_case import ConsultarChavePixPorHashUseCase
from pix.use_cases.criar_chave_pix_use_case import CriarChavePixUseCase
from pix.use_cases.criar_cobranca_pix_use_case import CriarTransferenciaPixUseCase
from pix.use_cases.devolver_pix_use_case import DevolverPixUseCase
from pix.use_cases.excluir_chave_pix_use_case import ExcluirChavePixUseCase
from pix.use_cases.pagar_pix_use_case import PagarPixUseCase


class CriarChavePixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chave_pix_use_case = CriarChavePixUseCase()

    @swagger_auto_schema(
        request_body=CriarChavePixInputSerializer(),
        responses={
            status.HTTP_201_CREATED: CriarChavePixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
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


class ConsultarChavesPixPorContaView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consultar_chave_pix_por_conta_use_case = ConsultarChavePixPorContaUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarChavePixPorContaInputSerializer(),
        responses={
            status.HTTP_200_OK: CriarChavePixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultarChavePixPorContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')

        chave_pix = self.consultar_chave_pix_por_conta_use_case.execute(agencia=agencia, num_conta=num_conta)

        output = CriarChavePixOutputSerializer(instance=chave_pix, many=True)

        return Response(data=output.data, status=status.HTTP_200_OK)


class ConsultarChavePixPeloHashView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consultar_chave_pix_pelo_hash_use_case = ConsultarChavePixPorHashUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarChavePixPeloHashInputSerializer(),
        responses={
            status.HTTP_200_OK: CriarChavePixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultarChavePixPeloHashInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        valor_chave = serializer.validated_data['valor_chave']

        chave_pix = self.consultar_chave_pix_pelo_hash_use_case.execute(valor_chave_pix=valor_chave)

        output = CriarChavePixOutputSerializer(instance=chave_pix)

        return Response(data=output.data, status=status.HTTP_200_OK)


class ExcluirChavePixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.excluir_conta_use_case = ExcluirChavePixUseCase()

    @swagger_auto_schema(
        request_body=ConsultarChavePixPeloHashInputSerializer(),
        responses={
            status.HTTP_200_OK: CriarChavePixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request):
        serializer = ConsultarChavePixPeloHashInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_chave = serializer.validated_data['valor_chave']

        chave_pix = self.excluir_conta_use_case.execute(valor_chave_pix=valor_chave)

        output = CriarChavePixOutputSerializer(instance=chave_pix)

        return Response(data=output.data, status=status.HTTP_200_OK)


class CriarCobrancaPixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.criar_pix_use_case = CriarTransferenciaPixUseCase()

    @swagger_auto_schema(
        request_body=CriarCobrancaPixInputSerializer(),
        responses={
            status.HTTP_201_CREATED: CriarCobrancaPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def post(self, request: Request):
        serializer = CriarCobrancaPixInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chave_pix_origem = serializer.validated_data['chave_pix_origem']
        chave_pix_destino = serializer.validated_data['chave_pix_destino']
        valor_transferencia = serializer.validated_data['valor_transferencia']
        validade = serializer.validated_data['validade']

        cobranca_pix = self.criar_pix_use_case.execute(chave_pix_origem=chave_pix_origem,
                                                       chave_pix_destino=chave_pix_destino,
                                                       valor=valor_transferencia, validade=validade)

        output = CriarCobrancaPixOutputSerializer(instance=cobranca_pix)

        return Response(data=output.data, status=status.HTTP_201_CREATED)


class PagarPixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagar_pix_use_case = PagarPixUseCase()

    @swagger_auto_schema(
        request_body=PagarPixInputSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: CriarCobrancaPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request):
        serializer = PagarPixInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_cobranca = serializer.validated_data['id_cobranca']

        pagamento = self.pagar_pix_use_case.execute(id_cobranca=id_cobranca)

        output = CriarCobrancaPixOutputSerializer(instance=pagamento)

        return Response(data=output.data, status=status.HTTP_202_ACCEPTED)


class DevolucaoPixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.devolver_pix_use_case = DevolverPixUseCase()

    @swagger_auto_schema(
        request_body=PagarPixInputSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: CriarCobrancaPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def patch(self, request: Request):
        serializer = DevolucaoPixInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_pagamento = serializer.validated_data['id_pagamento']
        valor_a_devolver = serializer.validated_data['valor_a_devolver']

        devolucao = self.devolver_pix_use_case.execute(id_pagamento=id_pagamento, valor_a_devolver=valor_a_devolver)

        output = DevolucaoPixOutputSerializer(instance=devolucao)
        return Response(data=output.data, status=status.HTTP_202_ACCEPTED)


class BuscarCobrancaPixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_cobranca_pix_use_case = BuscarCobrancaPixUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarChavePixPeloHashInputSerializer(),
        responses={
            status.HTTP_200_OK: CriarCobrancaPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultarChavePixPeloHashInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        chave_pix = serializer.validated_data['valor_chave']

        cobranca = self.buscar_cobranca_pix_use_case.execute(chave_pix=chave_pix)

        output = CriarCobrancaPixOutputSerializer(instance=cobranca, many=True)

        return Response(data=output.data, status=status.HTTP_200_OK)


class BuscarPagamentoPixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_pagamento_pix_use_case = BuscarPagamentoPixUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarChavePixPorContaInputSerializer(),
        responses={
            status.HTTP_200_OK: PagamentoPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultarChavePixPorContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')

        pagamento = self.buscar_pagamento_pix_use_case.execute(agencia_origem=agencia, num_conta_origem=num_conta)

        output = PagamentoPixOutputSerializer(instance=pagamento, many=True)

        return Response(data=output.data, status=status.HTTP_200_OK)


class BuscarRecebimentoPixView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_recebimento_pix_use_case = BuscarPagamentoPixUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarChavePixPorContaInputSerializer(),
        responses={
            status.HTTP_200_OK: PagamentoPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultarChavePixPorContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data['agencia']
        num_conta = serializer.validated_data['num_conta']

        pagamento = self.buscar_recebimento_pix_use_case.execute(agencia_destino=agencia, num_conta_destino=num_conta)

        output = PagamentoPixOutputSerializer(instance=pagamento, many=True)

        return Response(data=output.data, status=status.HTTP_200_OK)


class BuscarDevolucaoPixPelaOrigemView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_devolucao_pix_pela_origem_use_case = BuscarRecebivelPixUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarChavePixPorContaInputSerializer(),
        responses={
            status.HTTP_200_OK: DevolucaoPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultarChavePixPorContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')

        pagamento = self.buscar_devolucao_pix_pela_origem_use_case.execute(agencia_origem=agencia,
                                                                           num_conta_origem=num_conta)

        output = DevolucaoPixOutputSerializer(instance=pagamento, many=True)

        return Response(data=output.data, status=status.HTTP_200_OK)


class BuscarDevolucaoPixPeloDestinoView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_devolucao_pix_pelo_destino_use_case = BuscarRecebivelPixUseCase()

    @swagger_auto_schema(
        query_serializer=ConsultarChavePixPorContaInputSerializer(),
        responses={
            status.HTTP_200_OK: DevolucaoPixOutputSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad request.'
        }
    )
    def get(self, request: Request):
        serializer = ConsultarChavePixPorContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')

        pagamento = self.buscar_devolucao_pix_pelo_destino_use_case.execute(agencia_destino=agencia,
                                                                            num_conta_destino=num_conta)

        output = DevolucaoPixOutputSerializer(instance=pagamento, many=True)

        return Response(data=output.data, status=status.HTTP_200_OK)
