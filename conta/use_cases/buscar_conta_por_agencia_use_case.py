from rest_framework import status

from conta.exceptions.agencia_invalido import AgenciaInvalido
from conta.exceptions.agencia_is_None import AgenciaNulo
from conta.exceptions.num_conta_invalido import NumContaInvalido
from conta.exceptions.num_conta_is_none import NumContaNulo
from conta.models import ContaCorrente


class BuscarContaPorAgenciaUseCase:

    def execute(self, agencia: str, num_conta: str):
        conta_corrente = ContaCorrente.objects.get(agencia=agencia, num_conta=num_conta)
        return conta_corrente
