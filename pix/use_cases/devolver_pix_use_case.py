import uuid

from django.db import transaction
from rest_framework.exceptions import ValidationError

from pix.models import PagamentoPix, DevolucaoPix


class DevolverPixUseCase:
    def execute(self, id_pagamento: uuid.UUID, valor_a_devolver: float):

        # Busca o pagamento pelo id e identifica a conta que irá devolver o valor e a que irá receber o estorno
        conta_a_receber_devolucao = PagamentoPix.objects.get(id=id_pagamento).conta_origem.saldo
        conta_a_enviar_devolucao = PagamentoPix.objects.get(id=id_pagamento).conta_destino.saldo

        if conta_a_enviar_devolucao.saldo < valor_a_devolver:
            raise ValidationError({'Saldo': 'Saldo insuficiente para a operação desejada.'})

        with transaction.atomic():
            # Debita da conta que recebeu o pagamento o valor a ser devolvido e salva o novo saldo da conta
            conta_a_enviar_devolucao.saldo -= valor_a_devolver
            conta_a_enviar_devolucao.save()

            # Credita na conta que havia feito o pagamento e salva o novo saldo somando o valor recebido
            conta_a_receber_devolucao.saldo += valor_a_devolver
            conta_a_receber_devolucao.save()

        # Atualiza o status da cobranca para devolvido
        conta_a_receber_devolucao.status = 'Pagamento devolvido'
        conta_a_receber_devolucao.save()

        # Cria o objeto devolução
        return DevolucaoPix.objects.create(pagamento=id_pagamento)

