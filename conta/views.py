from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# from conta.factories import ContaCorrenteFactories
from conta.exceptions.agencia_invalido import AgenciaInvalido
from conta.exceptions.agencia_is_None import AgenciaNulo
from conta.exceptions.cpf_invalido_por_numero_de_caracteres import NumeroDeCaracteresCpf
from conta.exceptions.cpf_nao_informado import CpfNaoInformado
from conta.exceptions.id_conta_formato_inválido import IdContaFormatoInvalido
from conta.exceptions.num_conta_invalido import NumContaInvalido
from conta.exceptions.num_conta_is_none import NumContaNulo
from conta.exceptions.saldo_insuficiente import SaldoInsuficiente
from conta.serializers import CriarContaSerializer, ContaCorrenteSerializer, ConsultarContaOutputSerializer, \
    DepositoInputSerializer, SaqueInputSerializer, \
    MulticontaInputSerializer, ConsultarContaInputSerializer
from conta.use_cases.consultar_conta_use_case import ListarContaUseCase
from conta.use_cases.criar_conta_use_case import CriarContaUseCase
from conta.use_cases.deposito_use_case import DepositoUseCase
from conta.use_cases.multiconta_use_case import MulticontaUseCase
from conta.use_cases.saque_use_case import SaqueUseCase


class CriarContaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.criar_conta_use_case = CriarContaUseCase()

    def post(self, request):
        serializer = CriarContaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nome = serializer.validated_data['nome']
        cpf = serializer.validated_data['cpf']

        try:
            conta = self.criar_conta_use_case.execute(nome=nome, cpf=cpf)
        except (AgenciaInvalido, AgenciaNulo, NumContaInvalido, NumContaNulo, NumeroDeCaracteresCpf, CpfNaoInformado) \
                as exc:
            return Response(status=status.HTTP_404_NOT_FOUND, data=exc.args[0])

        output = ContaCorrenteSerializer(instance=conta)
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class ListarContaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listar_conta_use_case = ListarContaUseCase()

    def get(self, request: Request):
        serializer = ConsultarContaInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data.get('agencia')
        num_conta = serializer.validated_data.get('num_conta')
        id_conta = serializer.validated_data.get('id_conta')
        cpf = serializer.validated_data.get('cpf')

        try:
            conta_corrente = self.listar_conta_use_case.execute(agencia=agencia, num_conta=num_conta, cpf=cpf,
                                                                id_conta=id_conta)
        except (AgenciaInvalido, NumContaInvalido, IdContaFormatoInvalido) as exc:
            return Response(data=exc.args[0], status=status.HTTP_404_NOT_FOUND)

        output = ConsultarContaOutputSerializer(instance=conta_corrente, many=True)
        return Response(data=output.data, status='200')


class DepositoView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deposito_use_case = DepositoUseCase()

    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = DepositoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_deposito = serializer.validated_data['valor_deposito']

        try:
            conta_atualizada = self.deposito_use_case.execute(agencia=agencia, num_conta=num_conta,
                                                              valor_deposito=valor_deposito)
        except (AgenciaInvalido, NumContaInvalido, SaldoInsuficiente, AgenciaNulo, NumContaNulo) as exc:
            return Response(data=exc.args[0], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        output = ConsultarContaOutputSerializer(instance=conta_atualizada)
        return Response(data=output.data, status='202')


class SaqueView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.saque_use_case = SaqueUseCase()

    def patch(self, request: Request, agencia: str, num_conta: str):
        serializer = SaqueInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valor_saque = serializer.validated_data['valor_saque']

        try:
            conta_atualizada = self.saque_use_case.execute(agencia=agencia, num_conta=num_conta,
                                                           valor_saque=valor_saque)
        except (AgenciaInvalido, NumContaInvalido, SaldoInsuficiente, AgenciaNulo, NumContaNulo) as exc:
            return Response(data=exc.args[0], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        output = ConsultarContaOutputSerializer(instance=conta_atualizada)
        return Response(data=output.data, status='202')


class MulticontaView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.multiconta_use_case = MulticontaUseCase()

    def post(self, request: Request):
        serializer = MulticontaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agencia = serializer.validated_data['agencia']
        numero_conta_origem = serializer.validated_data['conta_origem']

        try:
            conta_corrente = self.multiconta_use_case.execute(agencia=agencia, num_conta=numero_conta_origem)
        except (AgenciaInvalido, NumContaInvalido, AgenciaNulo, NumContaNulo) as exc:
            return Response(data=exc.args[0], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        output = ConsultarContaOutputSerializer(instance=conta_corrente)
        return Response(data=output.data, status=200)

# class IdealConsultaContaView(APIView):
#     get_output_serializer = ConsultarContaOutputSerializer
#     get_sucess_status = 200
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._consultar_conta_use_case = ContaCorrenteFactories.make_consultar_conta_use_case()
#
#     def get(self, request, agencia, conta):
#         conta_corrente = self._consultar_conta_use_case.execute(agencia=agencia, conta=conta)
#
#         output = self.get_output_serializer(instance=conta_corrente)
#         return Response(data=output.data, status=self.get_sucess_status)
