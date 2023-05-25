import uuid

from boleto.exceptions import SaldoInsuficiente
from conta.service import buscar_conta_por_agencia
from transferencia.models import Transferencia


def transfer(agencia_origem, num_conta_origem, agencia_destino, num_conta_destino, valor):
    conta_origem = buscar_conta_por_agencia(agencia=agencia_origem, num_conta=num_conta_origem)
    if conta_origem.saldo < valor:
        raise SaldoInsuficiente('Saldo insuficiente para a operação solicitada.')

    conta_destino = buscar_conta_por_agencia(agencia=agencia_destino, num_conta=num_conta_destino)

    conta_origem.saldo -= valor
    conta_destino.saldo += valor
    conta_origem.save()
    conta_destino.save()

    transferencia = Transferencia.objects.create(conta_origem=conta_origem, conta_destino=conta_destino,
                                                 valor=valor)
    return transferencia


def consulta_transferencia(id_transferencia: uuid):
    transferencia = Transferencia.objects.get(id_transferencia=id_transferencia)
    return transferencia

