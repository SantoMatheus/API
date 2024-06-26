from conta.models import Saque


class BuscarSaqueUseCase:
    def execute(self, agencia: str, num_conta: str):
        return Saque.objects.filter(conta_corrente__agencia=agencia, conta_corrente__num_conta=num_conta)
