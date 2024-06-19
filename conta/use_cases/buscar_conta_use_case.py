import uuid
from typing import Optional

from django.db.models import Q

from conta.models import ContaCorrente


class BuscarContaUseCase:

    def execute(self, agencia: Optional[str] = None, num_conta: Optional[str] = None, cpf: Optional[str] = None,
                id_conta: Optional[uuid.uuid4] = None):

        consulta = Q()
        if agencia:
            consulta &= Q(agencia=agencia)
        if num_conta:
            consulta &= Q(num_conta=num_conta)
        if cpf:
            consulta &= Q(cpf=cpf)
        if id_conta:
            consulta &= Q(id=id_conta)

        return ContaCorrente.objects.get(consulta)
