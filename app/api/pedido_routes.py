from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.pedido_service import PedidoService
from app.api import schemas
from app.infrastructure.security import obter_usuario_atual
from app.domain import models
from app.domain.models import CanalPedido


# Rotas de pedidos
router = APIRouter()


# Criar pedido
@router.post("/pedidos")
def realizar_pedido(
    dados: schemas.PedidoCreate,
    db: Session = Depends(get_db),

    # Usuário autenticado
    usuario_atual: models.Usuario = Depends(obter_usuario_atual)
):

    # Cria pedido
    novo_pedido = PedidoService.criar_novo_pedido(
        db,
        usuario_atual.id,
        dados.canal_pedido,
        dados.produtos_ids
    )

    return {
        "mensagem": f"Pedido recebido! Usuário: {usuario_atual.nome}",
        "pedido": {
            "id": novo_pedido.id,
            "usuario_id": novo_pedido.usuario_id,
            "canal_pedido": novo_pedido.canal_pedido.value,
            "status": novo_pedido.status,
            "total": novo_pedido.total
        }
    }


# Simula pagamento mock
@router.post("/pagamentos/simular")
def pagar_pedido(
    dados: schemas.PagamentoSimulacao,
    db: Session = Depends(get_db),

    # Usuário autenticado
    usuario_atual: models.Usuario = Depends(obter_usuario_atual)
):

    # Atualiza pagamento
    pedido = PedidoService.simular_pagamento(
        db,
        dados.pedido_id,
        dados.sucesso,
        usuario_atual
    )

    return {
        "mensagem": "Pagamento processado com sucesso",
        "pedido_id": pedido.id,
        "status_atualizado": pedido.status
    }


# Listar pedidos
@router.get("/pedidos")
def listar_pedidos(
    canal_pedido: CanalPedido | None = None,
    db: Session = Depends(get_db),

    # Usuário autenticado
    usuario_atual: models.Usuario = Depends(obter_usuario_atual)
):

    pedidos = PedidoService.listar_pedidos(
        db=db,
        usuario=usuario_atual,
        canal_pedido=canal_pedido
    )

    return [
        {
            "id": pedido.id,
            "usuario_id": pedido.usuario_id,
            "canal_pedido": pedido.canal_pedido.value,
            "status": pedido.status,
            "total": pedido.total
        }
        for pedido in pedidos
    ]