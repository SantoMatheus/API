import uuid

from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase
from pix.exceptions.valor_chave_requerido import ValorChaveRequerido
from pix.models import ChavePix, TipoChavePixChoice


class CriarChavePixUseCase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_conta_use_case = BuscarContaUseCase()

    def execute(self, agencia: str, num_conta: str, tipo: str, valor_chave: str = None):
        if tipo == TipoChavePixChoice.EVP:
            valor_chave = uuid.uuid4()

        if tipo != TipoChavePixChoice.EVP and valor_chave is None:
            raise ValorChaveRequerido('Informe um valor compatível com o tipo selecionado.'
                                      'Somente chaves aleatórias do tipo EVP são autopreenchidas.')

        conta_corrente = self.buscar_conta_use_case.execute(agencia=agencia, num_conta=num_conta)
        chave_pix = ChavePix.objects.create(conta_corrente=conta_corrente, valor_chave=valor_chave, tipo=tipo)
        return chave_pix
