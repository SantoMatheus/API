import uuid
from typing import Optional

from django.db.models import Q

from conta.models import Transferencia


class ListarTransferenciaUseCase:
    def execute(self, agencia_origem: Optional[str] = None, num_conta_origem: Optional[str] = None,
                agencia_destino: Optional[str] = None, num_conta_destino: Optional[str] = None,
                id_transferencia: Optional[uuid.UUID] = None, valor: Optional[float] = None) -> Transferencia:

        consulta = Q()

        if agencia_origem:
            consulta &= Q(conta_origem__agencia=agencia_origem)
        if num_conta_origem:
            consulta &= Q(conta_origem__num_conta=num_conta_origem)
        if agencia_destino:
            consulta &= Q(conta_destino__agencia=agencia_destino)
        if num_conta_destino:
            consulta &= Q(conta_destino__Num_conta=num_conta_destino)
        if id_transferencia:
            consulta &= Q(id=id_transferencia)
        if valor:
            consulta &= Q(valor=valor)

        return Transferencia.objects.filter(consulta)

