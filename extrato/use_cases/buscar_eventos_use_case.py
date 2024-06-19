from itertools import chain
from operator import attrgetter
from typing import Optional

from boleto.models import PagamentoBoleto
from conta.models import Saque, Deposito
from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase
from pix.models import PagamentoPix, DevolucaoPix
from transferencia.models import Transferencia


class BuscarEventosUseCase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listar_boleto_use_case = BuscarContaUseCase()

    def execute(self, agencia: str, conta_corrente: str):
        boletos = PagamentoBoleto.objects.filter(boleto__agencia=agencia, boleto__num_conta=conta_corrente)

        pix = PagamentoPix.objects.filter(conta_origem__agencia=agencia, conta_origem__num_conta=conta_corrente)

        devolucao_pix = DevolucaoPix.objects.filter(pagamento__cobranca_pix__agencia=agencia,
                                                    pagamento__cobranca_pix__conta_origem=conta_corrente)

        transferencia = Transferencia.objects.filter(conta_origem__agencia=agencia,
                                                     conta_origem__num_conta=conta_corrente)
        saque = Saque.objects.filter(conta_corrente__agencia=agencia, conta_corrente__conta_corrente=conta_corrente)

        deposito = Deposito.objects.filter(conta_corrente__agencia=agencia,
                                           conta_corrente__conta_corrente=conta_corrente)

        all_transactions = sorted(chain(boletos, pix, devolucao_pix, transferencia, saque, deposito),
                                  key=attrgetter('create'))
        return all_transactions
