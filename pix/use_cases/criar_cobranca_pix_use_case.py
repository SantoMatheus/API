from datetime import datetime

from common_modules.definir_vencimento_cobranca_use_case import DefinirVencimentoCobrancaUseCase
from pix.models import TransferenciaPix
from pix.use_cases.consultar_chave_pix_por_hash_use_case import ConsultarChavePixPorHashUseCase


class CriarTransferenciaPixUseCase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consultar_chave_pix_por_hash = ConsultarChavePixPorHashUseCase()
        self.definir_vencimento_use_case = DefinirVencimentoCobrancaUseCase()

    def execute(self, chave_pix_origem: str, chave_pix_destino: str, valor: float, validade: str):
        # Busca os dados da conta de onde a transferência irá partir
        chave_pix_origem = self.consultar_chave_pix_por_hash.execute(valor_chave_pix=chave_pix_origem).conta_corrente
        # Busca a conta para onde a transferência será enviada
        chave_pix_destino = self.consultar_chave_pix_por_hash.execute(valor_chave_pix=chave_pix_destino)
        # Define a data de vencimento
        vencimento = self.definir_vencimento_use_case.execute(dias_ate_expirar=validade)
        # Cria o objeto transferência
        return TransferenciaPix.objects.create(conta_origem=chave_pix_origem,
                                               conta_destino=chave_pix_destino, valor=valor,
                                               valido_ate=vencimento)
