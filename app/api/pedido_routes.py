from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.pedido_service import PedidoService
from app.api import schemas
from app.infrastructure.security import obter_usuario_atual
from app.domain import models

# rotas de pedidos
router = APIRouter()

# criar pedido
@router.post("/pedidos")
def realizar_pedido(
    dados: schemas.PedidoCreate,
    db: Session = Depends(get_db),

    # usuario autenticado
    usuario_atual: models.Usuario = Depends(obter_usuario_atual)
):

    # cria pedido
    novo_pedido = PedidoService.criar_novo_pedido(
        db,
        usuario_atual.id,
        dados.canal_pedido,
        dados.produtos_ids
    )

    return {
        "mensagem": f"Pedido recebido! Usuário: {usuario_atual.nome}",
        "pedido": novo_pedido
    }

# simula pagamento
@router.post("/pagamentos/simular")
def pagar_pedido(dados: schemas.PagamentoSimulacao, db: Session = Depends(get_db)):

    # atualiza pagamento
    pedido = PedidoService.simular_pagamento(
        db,
        dados.pedido_id,
        dados.sucesso
    )

    # verifica pedido
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return {"status_atualizado": pedido.status}

# listar pedidos
@router.get("/pedidos")
def listar_pedidos(db: Session = Depends(get_db)):

    pedidos = PedidoService.listar_todos(db)

    return pedidos