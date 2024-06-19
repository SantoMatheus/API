
from django.utils import timezone

from boleto.models import Boleto
from pix.models import TransferenciaPix


def atualiza_status_para_vencido():
    agora = timezone.now()

    # Busca as cobranças pix vencidas e atualiza o status para 'vencido' salvando o novo status
    cobrancas_pix_expiradas = TransferenciaPix.objects.filter(valido_ate__lte=agora,
                                                              status='aguardando_pagamento')
    for cobranca in cobrancas_pix_expiradas:
        cobranca.status = 'vencido'
        cobranca.save()

    # Busca os boletos vencidos e atualiza o status para 'vencido' salvando o novo status
    cobrancas_boleto_expiradas = Boleto.objects.filter(vencimento__lte=agora, status='aguardando_pagamento')
    for boleto in cobrancas_boleto_expiradas:
        boleto.status = 'vencido'
        boleto.save()
