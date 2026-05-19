from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.pedido_service import PedidoService
from app.api import schemas
from app.infrastructure.security import obter_usuario_atual 
from app.domain import models

# Aqui a gente cria o grupo de rotas pra não deixar tudo solto no arquivo principal
router = APIRouter()

# Rota para criar um pedido novo (POST)
@router.post("/pedidos")
def realizar_pedido(
    dados: schemas.PedidoCreate, # O que o usuário envia no corpo do JSON
    db: Session = Depends(get_db), # Abre a conexão com o banco de dados automaticamente
    
    # Isso aqui verifica se o token do usuário é válido antes de deixar ele seguir
    usuario_atual: models.Usuario = Depends(obter_usuario_atual) 
):

    # Mandando os dados lá para o PedidoService fazer o trabalho pesado de salvar
    novo_pedido = PedidoService.criar_novo_pedido(
        db, 
        usuario_atual.id, # Pega o ID do usuário que acabou de logar
        dados.canal_pedido, 
        dados.produtos_ids
    )
    
    # Retorna uma mensagem de sucesso pro front-end
    return {
        "mensagem": f"Pedido recebido! Usuário autenticado: {usuario_atual.nome}", 
        "pedido": novo_pedido
    }

# Rota para fingir que o pagamento foi feito e mudar o status
@router.post("/pagamentos/simular")
def pagar_pedido(dados: schemas.PagamentoSimulacao, db: Session = Depends(get_db)):
    pedido = PedidoService.simular_pagamento(db, dados.pedido_id, dados.sucesso)
    
    # Se o ID do pedido estiver errado, a gente avisa que não achou (Erro 404)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Mostra na tela o novo status (ex: Pago ou Cancelado)
    return {"status_atualizado": pedido.status}

# Rota simples só para ver todos os pedidos que já foram feitos
@router.get("/pedidos")
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = PedidoService.listar_todos(db)
    return pedidos # Devolve a lista completa de pedidos
