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
            parametros_conta['agencia'] = agencia

        if num_conta:
            parametros_conta['num_conta'] = num_conta

        if id_conta:
            parametros_conta['id'] = id_conta

        if cpf:
            parametros_conta['cpf'] = cpf

        conta_corrente = ContaCorrente.objects.filter(**parametros_conta)
        return conta_corrente
