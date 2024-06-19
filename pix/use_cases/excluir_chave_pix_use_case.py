from pix.use_cases.consultar_chave_pix_por_hash_use_case import ConsultarChavePixPorHashUseCase


class ExcluirChavePixUseCase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consultar_chave_pix_por_hash = ConsultarChavePixPorHashUseCase()

    def execute(self, valor_chave_pix):
        chave_pix = self.consultar_chave_pix_por_hash.execute(valor_chave_pix=valor_chave_pix)
        chave_pix.esta_ativa = False
        chave_pix.save()
        return chave_pix

