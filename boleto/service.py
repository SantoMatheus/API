import uuid
from datetime import date

from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.models import Boleto
from conta.models import ContaCorrente
from conta.service import buscar_conta_por_agencia


def gerar_boleto(num_conta, agencia, valor, data_vencimento):
    conta_corrente = buscar_conta_por_agencia(agencia=agencia, num_conta=num_conta)
    boleto = Boleto.objects.create(conta_corrente=conta_corrente, valor=valor, data_vencimento=data_vencimento)
    return boleto


def listar_boletos(agencia=None, num_conta=None, pago=None, id_boleto=None):
    parametros_conta = {}
    if agencia:
        parametros_conta['agencia'] = agencia
    if num_conta:
        parametros_conta['num_conta'] = num_conta
    contas_correntes = ContaCorrente.objects.filter(**parametros_conta)

    parametros_boleto = {}
    if pago:
        parametros_boleto['pago'] = pago
    if id_boleto:
        parametros_boleto['id'] = id_boleto
    boletos = Boleto.objects.filter(conta_corrente__in=contas_correntes, **parametros_boleto)

    return boletos


def consulta_boleto(id_boleto, agencia, num_conta):
    conta_corrente = buscar_conta_por_agencia(agencia=agencia, num_conta=num_conta)
    boleto = Boleto.objects.get(conta_corrente=conta_corrente, id=id_boleto)
    return boleto


def pagar_boleto(id_boleto, num_conta, agencia):
    boleto = consulta_boleto(id_boleto=id_boleto, num_conta=num_conta, agencia=agencia)
    saldo = boleto.conta_corrente.saldo
    pagamento = boleto.valor

    if boleto.status == 'Pago':
        raise BoletoPago('Boleto já liquidado.')

    if saldo <= pagamento:
        raise SaldoInsuficiente('Saldo insuficiente para este pagamento.')

    boleto.conta_corrente.saldo -= pagamento
    boleto.status = 'Pago'
    boleto.pago = True
    boleto.save()
    boleto.conta_corrente.save()
    return boleto


def cancelar_boleto(id_boleto: uuid.UUID, agencia: str, num_conta: str) -> Boleto:
    boleto = consulta_boleto(id_boleto=id_boleto, agencia=agencia, num_conta=num_conta)
    if boleto.status == 'Pago':
        raise BoletoPago('Boleto pagos não podem ser cancelados.')

    boleto.status = 'Cancelado'
    boleto.save()
    return boleto
