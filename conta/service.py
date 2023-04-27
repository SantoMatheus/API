from conta.models import ContaCorrente


def criar_conta(nome, cpf) -> ContaCorrente:
    num_conta = gerar_num_conta()
    conta_criada = ContaCorrente.objects.create(nome=nome, cpf=cpf, agencia='0001', num_conta=num_conta)
    return conta_criada


def gerar_num_conta() -> str:
    ultima_conta_criada = ContaCorrente.objects.all().order_by('created').last()
    if ultima_conta_criada is None:
        return '1'
    ultimo_num_conta = ultima_conta_criada.num_conta
    num_conta = int(ultimo_num_conta) + 1
    return str(num_conta)


def consultar_conta(agencia, num_conta) -> ContaCorrente:
    info_conta = ContaCorrente.objects.get(agencia=agencia, num_conta=num_conta)
    return info_conta


def aumentar_saldo(agencia, num_conta, valor_deposito):
    conta_destino = consultar_conta(agencia=agencia, num_conta=num_conta)
    conta_destino.saldo += valor_deposito
    conta_destino.save()

    return conta_destino

def diminuir_saldo(agencia, num_conta, valor_saque):
    conta_origem = consultar_conta(agencia=agencia, num_conta=num_conta)
    conta_origem.saldo -= valor_saque
    conta_origem.save()

    return conta_origem