from pix.models import ChavePix


class ConsultarChavePixPorHashUseCase:
    def execute(self, valor_chave_pix):
        chave_pix = ChavePix.objects.get(valor_chave=valor_chave_pix)
        return chave_pix
