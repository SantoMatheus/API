from conta.exceptions.cpf_invalido_por_numero_de_caracteres import NumeroDeCaracteresCpf
from conta.exceptions.cpf_nao_informado import CpfNaoInformado
from conta.exceptions.entrada_nao_numerica_cpf import CpfNaoNumerico
from conta.models import ContaCorrente
from conta.repositories import ContaCorrenteRepository
from conta.use_cases.gerar_num_conta_use_case import GerarNumContaUseCase


class CriarContaUseCase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gerar_num_conta_use_case = GerarNumContaUseCase()

    def execute(self, nome: str, cpf: str) -> ContaCorrente:
        if len(cpf) != 11:
            raise NumeroDeCaracteresCpf("Informe um número de CPF válido.")
        if cpf.isdigit() is False:
            raise CpfNaoNumerico('Informe apenas os números do CPF.')
        if cpf is None:
            raise CpfNaoInformado('Informe algum valor para o CPF. Apenas os números.')

        num_conta = self.gerar_num_conta_use_case.execute()
        conta_criada = ContaCorrente.objects.create(nome=nome, cpf=cpf, agencia='0001', num_conta=num_conta)
        return conta_criada

# class ConsultarContaUseCase:
#     def __init__(self, conta_corrente_repository: ContaCorrenteRepository):
#         self._conta_corrente_repository = conta_corrente_repository
#
#     def execute(self, agencia: str, conta: str) -> ContaCorrente:
#         conta_corrente = self.__find_in_db(agencia=agencia, conta=conta)
#         return conta_corrente
#
#     def __find_in_db(self, agencia: str, conta: str):
#         return self._conta_corrente_repository.find_by_agencia_and_conta(agencia=agencia, conta=conta)
