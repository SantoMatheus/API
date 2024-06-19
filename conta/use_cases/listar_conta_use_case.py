import uuid
from typing import Optional

from django.db.models import Q

from conta.models import ContaCorrente


class ListarContaUseCase:

    def execute(self, agencia: Optional[str] = None, num_conta: Optional[str] = None,
                id_conta: Optional[uuid.UUID] = None, cpf: Optional[str] = None, nome_responsavel: Optional[str] = None):

        consulta = Q()
        if agencia:
            consulta &= Q(agencia=agencia)

        if num_conta:
            consulta &= Q(num_conta=num_conta)

        if id_conta:
            consulta &= Q(id=id_conta)

        if cpf:
            consulta &= Q(cpf=cpf)
        if nome_responsavel:
            consulta &= Q(nome=nome_responsavel)

        return ContaCorrente.objects.filter(consulta)
