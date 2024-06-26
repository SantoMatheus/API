from typing import Optional

from django.db.models import Q

from pix.models import PagamentoPix


class BuscarPagamentoPixUseCase:
    def execute(self, agencia_origem: Optional[str] = None, num_conta_origem: Optional[str] = None,
                agencia_destino: Optional[str] = None, num_conta_destino: Optional[str] = None):

        parametros_pagamento = Q()
        if agencia_destino:
            parametros_pagamento &= Q(cobranca_pix__conta_destino__conta_corrente__agencia=agencia_destino)
        if num_conta_destino:
            parametros_pagamento &= Q(cobranca_pix__conta_destino__conta_corrente__num_conta=num_conta_destino)
        if agencia_origem:
            parametros_pagamento &= Q(cobranca_pix__conta_origem__agencia=agencia_origem)
        if num_conta_origem:
            parametros_pagamento &= Q(cobranca_pix__conta_origem__num_conta=num_conta_origem)

        pagamento_pix = PagamentoPix.objects.filter(parametros_pagamento)
        return pagamento_pix
