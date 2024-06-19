import uuid
from typing import Optional

from conta.use_cases.buscar_conta_use_case import BuscarContaUseCase


class CancelarContaUseCase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buscar_conta_use_case = BuscarContaUseCase()

    def execute(self, agencia: Optional[str] = None, num_conta: Optional[str] = None, cpf: Optional[str] = None,
                id_conta: Optional[uuid.uuid4] = None):
        conta_corrente = self.buscar_conta_use_case.execute(agencia=agencia, num_conta=num_conta, cpf=cpf,
                                                            id_conta=id_conta)
        conta_corrente.status = 'cancelado'
        conta_corrente.save()
        return conta_corrente
