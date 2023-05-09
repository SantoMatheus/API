from conta.models import ContaCorrente


class ContaCorrenteRepository:
    model = ContaCorrente

    def find_by_agencia_and_conta(self, agencia, conta):
        return self.model.objects.get(agencia=agencia, num_conta=conta)
