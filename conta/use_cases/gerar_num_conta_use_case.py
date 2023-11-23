from conta.models import ContaCorrente


class GerarNumContaUseCase:

    def execute(self):
        ultima_conta_criada = ContaCorrente.objects.all().order_by('created').last()

        if ultima_conta_criada is None:
            return '1'

        ultimo_num_conta = int(ultima_conta_criada.num_conta) + 1
        num_conta = str(ultimo_num_conta)
        return num_conta




