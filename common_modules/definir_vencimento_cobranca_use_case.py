from datetime import timedelta

from django.utils import timezone


class DefinirVencimentoCobrancaUseCase:
    @staticmethod
    def execute(dias_ate_expirar: int):
        return timezone.now() + timedelta(days=dias_ate_expirar)
