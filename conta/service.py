from conta.models import ContaCorrente


def consultar_conta(agencia=None, num_conta=None, id_conta=None, cpf=None) -> ContaCorrente:
    parametros_conta = {}
    if agencia:
        parametros_conta['agencia'] = agencia
    if num_conta:
        parametros_conta['num_conta'] = num_conta
    if id_conta:
        parametros_conta['id'] = id_conta
    if cpf:
        parametros_conta['cpf'] = cpf

    conta_corrente = ContaCorrente.objects.filter(**parametros_conta)

    return conta_corrente


def aumentar_saldo(agencia, num_conta, valor_deposito) -> ContaCorrente:
    conta_corrente = buscar_conta_por_agencia(agencia=agencia, num_conta=num_conta)
    conta_corrente.saldo += valor_deposito
    conta_corrente.save()

    return conta_corrente


def diminuir_saldo(agencia, num_conta, valor_saque) -> ContaCorrente:
    conta_corrente = buscar_conta_por_agencia(agencia=agencia, num_conta=num_conta)
    conta_corrente.saldo -= valor_saque
    conta_corrente.save()

    return conta_corrente


def multiconta(agencia, num_conta):
    conta_corrente = buscar_conta_por_agencia(agencia=agencia, num_conta=num_conta)
    nova_conta = criar_conta(nome=conta_corrente.nome, cpf=conta_corrente.cpf)
    return nova_conta


def buscar_conta_por_agencia(agencia: str, num_conta: str) -> ContaCorrente:
    conta_corrente = ContaCorrente.objects.get(agencia=agencia, num_conta=num_conta)
    return conta_corrente
