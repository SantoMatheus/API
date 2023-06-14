import uuid

from conta.exceptions.cpf_invalido_por_numero_de_caracteres import NumeroDeCaracteresCpf
from conta.exceptions.cpf_nao_informado import CpfNaoInformado
from conta.exceptions.entrada_nao_numerica_cpf import CpfNaoNumerico
from conta.models import ContaCorrente


class ConsultarContaUseCase:
    def execute(self, agencia: str = None,num_conta: str = None, id_conta: uuid.UUID = None,
                cpf: str = None) -> ContaCorrente:
        parametros_conta = {}
        if agencia:
            parametros_conta['agencia'] = agencia
        if num_conta:
            parametros_conta['num_conta'] = num_conta
        if id_conta:
            parametros_conta['id_conta'] = id_conta
        if cpf:
            if len(cpf) != 11:
                raise NumeroDeCaracteresCpf("Informe um número de CPF válido.")
            if cpf.isdigit() is False:
                raise CpfNaoNumerico('Informe apenas os números do CPF.')
            parametros_conta['cpf'] = cpf

        conta_corrente = ContaCorrente.objects.filter(**parametros_conta)
        return conta_corrente
