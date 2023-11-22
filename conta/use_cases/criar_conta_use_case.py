
from conta.exceptions.cpf_invalido_por_numero_de_caracteres import NumeroDeCaracteresCpf
from conta.exceptions.cpf_invalido_por_tipo_de_caracter import CpfInvalidoTipoCaracter
from conta.exceptions.cpf_nao_informado import CpfNaoInformado
from conta.models import ContaCorrente
from conta.use_cases.gerar_num_conta_use_case import GerarNumContaUseCase


class CriarContaUseCase:

    def __init__(self):
        self.gerar_num_conta_use_case = GerarNumContaUseCase()

    def execute(self, nome: str, cpf: str) -> ContaCorrente:
        num_conta = self.gerar_num_conta_use_case.execute()
        conta_criada = ContaCorrente.objects.create(nome=nome, cpf=cpf, agencia='0001', num_conta=num_conta)
        return conta_criada


