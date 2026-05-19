from pydantic import BaseModel
from typing import List
from app.domain.models import CanalPedido 

class PedidoCreate(BaseModel):
    usuario_id: int
    canal_pedido: CanalPedido 
    produtos_ids: List[int]

class PagamentoSimulacao(BaseModel):
    pedido_id: int
    sucesso: bool
