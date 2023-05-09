from boleto.exceptions import BoletoPago, SaldoInsuficiente
from boleto.models import Boleto
from conta.service import consultar_conta


def gerar_boleto(num_conta, agencia, valor, data_vencimento):
    conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta)
    boleto = Boleto.objects.create(conta_corrente=conta_corrente, valor=valor, data_vencimento=data_vencimento)
    return boleto


def listar_boletos(agencia, num_conta):
    conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta)
    boletos = Boleto.objects.filter(conta_corrente=conta_corrente)
    return boletos


def consulta_boleto(id_boleto, agencia, num_conta):
    conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta)
    boleto = Boleto.objects.get(conta_corrente=conta_corrente, id=id_boleto)
    return boleto


def pagar_boleto(id_boleto, num_conta, agencia):
    boleto = consulta_boleto(id_boleto=id_boleto, num_conta=num_conta, agencia=agencia)
    saldo = boleto.conta_corrente.saldo
    pagamento = boleto.valor

    if boleto.pago is True:
        raise BoletoPago('Boleto já liquidado.')

    if saldo <= pagamento:
        raise SaldoInsuficiente('Saldo insuficiente para este pagamento.')

    boleto.conta_corrente.saldo -= pagamento
    boleto.pago = True
    boleto.save()
    boleto.conta_corrente.save()
    return boleto
