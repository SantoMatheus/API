import uuid

from conta.exceptions.agencia_invalido import AgenciaInvalido
from conta.exceptions.cpf_invalido_por_numero_de_caracteres import NumeroDeCaracteresCpf
from conta.exceptions.id_conta_formato_inválido import IdContaFormatoInvalido
from conta.exceptions.num_conta_invalido import NumContaInvalido
from conta.models import ContaCorrente


class ListarContaUseCase:

    def execute(self, agencia: str = None, num_conta: str = None, id_conta: uuid.UUID = None, cpf: str = None):
        parametros_conta = {}
        if agencia:
            if agencia is not True:
                raise AgenciaInvalido('Informe um número de agencia válido.')
            parametros_conta['agencia'] = agencia

        if num_conta:
            if num_conta is not True:
                raise NumContaInvalido('Informe um número de conta válido.')
            parametros_conta['num_conta'] = num_conta

        if id_conta:
            if id_conta != uuid.UUID:
                raise IdContaFormatoInvalido('Informe um número de ID válido para a conta.')
            parametros_conta['id'] = id_conta

        if cpf:
            if len(cpf) != 11:
                raise NumeroDeCaracteresCpf("Informe um número de CPF válido.")
            parametros_conta['cpf'] = cpf

        conta_corrente = ContaCorrente.objects.filter(**parametros_conta)
        return conta_corrente
