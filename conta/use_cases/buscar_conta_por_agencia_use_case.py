from rest_framework import status

from conta.exceptions.agencia_invalido import AgenciaInvalido
from conta.exceptions.agencia_is_None import AgenciaNulo
from conta.exceptions.num_conta_invalido import NumContaInvalido
from conta.exceptions.num_conta_is_none import NumContaNulo
from conta.models import ContaCorrente


class BuscarContaPorAgenciaUseCase:

    def execute(self, agencia: str, num_conta: str):
        if agencia is None:
            raise AgenciaNulo('Informe um número de agencia.')
        if num_conta is None:
            raise NumContaNulo('Informe um número de conta.')
        if agencia is not True:
            raise AgenciaInvalido('Informe um número de agencia válido.')
        if num_conta is not True:
            raise NumContaInvalido('Informe um número de conta válido.')

        conta_corrente = ContaCorrente.objects.get(agencia=agencia, num_conta=num_conta)
        return conta_corrente
