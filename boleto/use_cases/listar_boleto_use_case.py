import uuid
from datetime import datetime
from typing import Optional

from django.db.models import Q

from boleto.models import Boleto


class ListarBoletoUseCase:

    def execute(self, agencia: Optional[str] = None, id_conta: Optional[uuid.UUID] = None,
                num_conta: Optional[str] = None, status: Optional[str] = None,
                id_boleto: Optional[uuid.UUID] = None, valor: Optional[float] = None,
                data_de_vencimento: Optional[datetime] = None):
        filtro = Q()

        if agencia:
            filtro &= Q(conta_corrente__agencia=agencia)
        if id_conta:
            filtro &= Q(id_conta=id_conta)
        if status:
            filtro &= Q(status=status)
        if id_boleto:
            filtro &= Q(id_boleto=id_boleto)
        if valor:
            filtro &= Q(valor=valor)
        if data_de_vencimento:
            filtro &= Q(data_de_vencimento=data_de_vencimento)
        if num_conta:
            filtro &= Q(conta_corrente__num_conta=num_conta)

        return Boleto.objects.filter(filtro)
