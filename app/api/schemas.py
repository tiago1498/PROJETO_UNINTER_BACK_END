from pydantic import BaseModel
from typing import List
from app.domain.models import CanalPedido 

class PedidoCreate(BaseModel):
    canal_pedido: CanalPedido 
    produtos_ids: List[int]

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    perfil: str = "CLIENTE"

class PagamentoSimulacao(BaseModel):
    pedido_id: int
    sucesso: bool

