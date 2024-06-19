import uuid

from django.db import transaction
from rest_framework.exceptions import ValidationError

from pix.models import TransferenciaPix, PagamentoPix


class PagarPixUseCase:
    def execute(self, id_cobranca: uuid.UUID):

        # Busca a cobrança pelo id e identifica a conta que irá debitar o valor e a que irá receber o valor
        transferencia_pix = TransferenciaPix.objects.get(id=id_cobranca)
        conta_origem = transferencia_pix.conta_origem
        conta_destino = transferencia_pix.conta_destino.conta_corrente

        status_erros = {
            'vencido': 'Não é possível realizar o pagamento de cobranças vencidas.',
            'pago': 'Pagamento já efetuado.',
            'cancelado': 'Não é possível realizar o pagamento de cobranças canceladas.'
        }

        if transferencia_pix.status in status_erros:
            raise ValidationError({'Status': status_erros[transferencia_pix.status]})

        if conta_origem.saldo < transferencia_pix.valor:
            raise ValidationError({'Saldo': 'Saldo insuficiente para a operação desejada.'})

        # recebedor = TransferenciaPix.objects.get(id=id_cobranca)
        # conta_destino = recebedor.conta_destino

        with transaction.atomic():
            # Debita da conta de origem e salva o novo saldo subtraindo o valor pago
            conta_origem.saldo -= transferencia_pix.valor
            conta_origem.save()

            # Credita na conta destino e salva o novo saldo somando o valor recebido
            conta_destino.saldo += transferencia_pix.valor
            conta_destino.save()

        # Atualiza o status da cobranca para pago
        transferencia_pix.status = 'pago'
        transferencia_pix.save()

        # Cria o objeto pagamento
        return PagamentoPix.objects.create(cobranca_pix=id_cobranca)

