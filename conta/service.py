from conta.models import ContaCorrente, Boleto


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
    conta_corrente = ContaCorrente.objects.get(agencia=agencia, num_conta=num_conta)
    return conta_corrente


def aumentar_saldo(agencia, num_conta, valor_deposito) -> ContaCorrente:
    conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta)
    conta_corrente.saldo += valor_deposito
    conta_corrente.save()

    return conta_corrente


def diminuir_saldo(agencia, num_conta, valor_saque) -> ContaCorrente:
    conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta)
    conta_corrente.saldo -= valor_saque
    conta_corrente.save()

    return conta_corrente


def transferir_saldo(agencia_origem, conta_origem, valor, agencia_destino, conta_destino):
    conta_corrente = diminuir_saldo(agencia=agencia_origem, num_conta=conta_origem, valor_saque=valor)
    aumentar_saldo(agencia=agencia_destino, num_conta=conta_destino, valor_deposito=valor)
    return conta_corrente


def gerar_boleto(num_conta, agencia, valor, data_vencimento):
    conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta)
    boleto = Boleto.objects.create(conta_corrente=conta_corrente, valor=valor, data_vencimento=data_vencimento)
    return boleto
