from itertools import chain
from operator import attrgetter


from boleto.models import PagamentoBoleto
from boleto.serializers import PagamentoBoletoOutputSerializer
from boleto.use_cases.buscar_pagamento_boleto_use_case import BuscarPagamentoBoletoUseCase
from boleto.use_cases.buscar_recebimento_boleto_use_case import BuscarRecebimentoBoletoUseCase
from conta.models import Saque, Deposito
from conta.models import Transferencia
from conta.serializers import SaqueOutputSerializer, DepositoOutputSerializer, TransferenciaOutputSerializer
from conta.use_cases.buscar_deposito_use_case import BuscarDepositoUseCase
from conta.use_cases.buscar_saque_use_case import BuscarSaqueUseCase
from conta.use_cases.listar_transferencia_use_case import ListarTransferenciaUseCase
from pix.models import PagamentoPix, DevolucaoPix
from pix.serializers import PagamentoPixOutputSerializer, DevolucaoPixOutputSerializer
from pix.use_cases.buscar_devolucao_pix_use_case import BuscarDevolucaoPixUseCase
from pix.use_cases.buscar_pagamento_pix_use_case import BuscarPagamentoPixUseCase


class BuscarEventosUseCase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_pagamento_boleto_use_case = BuscarPagamentoBoletoUseCase()
        self.buscar_recebimento_boleto_use_case = BuscarRecebimentoBoletoUseCase()
        self.buscar_pagamento_pix_use_case = BuscarPagamentoPixUseCase()
        self.buscar_devolucao_pix_use_case = BuscarDevolucaoPixUseCase()
        self.buscar_saque_use_case = BuscarSaqueUseCase()
        self.buscar_deposito_use_case = BuscarDepositoUseCase()
        self.buscar_transferencia_use_case = ListarTransferenciaUseCase()

    def execute(self, agencia: str, conta_corrente: str):

        pagamento_boleto = self.buscar_pagamento_boleto_use_case.execute(agencia_sacado=agencia,
                                                                         num_conta_sacado=conta_corrente)

        recebimento_boleto = self.buscar_recebimento_boleto_use_case.execute(agencia_cedente=agencia,
                                                                             num_conta_cedente=conta_corrente)

        recebimento_pix = self.buscar_pagamento_pix_use_case.execute(agencia_destino=agencia,
                                                                     num_conta_destino=conta_corrente)

        devolucao_pix = self.buscar_devolucao_pix_use_case.execute(agencia=agencia,
                                                                   num_conta=conta_corrente)

        pagamento_pix = self.buscar_pagamento_pix_use_case.execute(agencia_origem=agencia,
                                                                   num_conta_origem=conta_corrente)

        transferencia_cash_in = self.buscar_transferencia_use_case.execute(agencia_destino=agencia,
                                                                           num_conta_destino=conta_corrente)

        transferencia_cash_out = self.buscar_transferencia_use_case.execute(agencia_origem=agencia,
                                                                            num_conta_origem=conta_corrente)

        saque = self.buscar_saque_use_case.execute(agencia=agencia, num_conta=conta_corrente)

        deposito = self.buscar_deposito_use_case.execute(agencia=agencia, num_conta=conta_corrente)

        eventos = (sorted(
            chain(pagamento_boleto, recebimento_boleto, pagamento_pix, recebimento_pix, devolucao_pix, transferencia_cash_in,
                  transferencia_cash_out, saque, deposito), key=attrgetter('criado_em')))

        def evento_serializer(evento):
            if isinstance(evento, PagamentoBoleto):
                return PagamentoBoletoOutputSerializer(evento).data
            elif isinstance(evento, PagamentoPix):
                return PagamentoPixOutputSerializer(evento).data
            elif isinstance(evento, DevolucaoPix):
                return DevolucaoPixOutputSerializer(evento).data
            elif isinstance(evento, Saque):
                return SaqueOutputSerializer(evento).data
            elif isinstance(evento, Deposito):
                return DepositoOutputSerializer(evento).data
            elif isinstance(evento, Transferencia):
                return TransferenciaOutputSerializer(evento).data

        eventos_serializados = [evento_serializer(evento) for evento in eventos]
        return eventos_serializados
