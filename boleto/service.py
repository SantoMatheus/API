from boleto.models import Boleto
from conta.service import consultar_conta


def gerar_boleto(num_conta, agencia, valor, data_vencimento):
    conta_corrente = consultar_conta(agencia=agencia, num_conta=num_conta)
    boleto = Boleto.objects.create(conta_corrente=conta_corrente, valor=valor, data_vencimento=data_vencimento)
    return boleto
