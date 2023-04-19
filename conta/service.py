from conta.models import ContaCorrente


def criar_conta(nome, cpf):
    num_conta = gerar_num_conta()
    conta_criada = ContaCorrente.objects.create(nome=nome, cpf=cpf, agencia='0001', num_conta=num_conta)
    return conta_criada


def gerar_num_conta():
    ultima_conta_criada = ContaCorrente.objects.all().order_by('created').last()
    if ultima_conta_criada is None:
        return '1'
    ultimo_num_conta = ultima_conta_criada.num_conta
    num_conta = int(ultimo_num_conta) + 1
    return str(num_conta)


def consultar_conta(agencia, num_conta):
    info_conta = ContaCorrente.objects.get(agencia=agencia, num_conta=num_conta)
    return info_conta

def DepositoConta(saldo):
       saldo_atual = ContaCorrente.objects.get(saldo=saldo)
       novo_saldo = ContaCorrente.objects.update(saldo_atual)
       return float(novo_saldo)
