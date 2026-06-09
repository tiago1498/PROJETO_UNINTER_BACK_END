from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.domain import models


# Serviço de pedidos
class PedidoService:

    @staticmethod
    def criar_novo_pedido(db: Session, usuario_id: int, canal: models.CanalPedido, itens: list):
        
        # Validação simples para não permitir pedido sem itens
        if not itens or len(itens) == 0:
            raise HTTPException(status_code=422, detail="O pedido deve possuir pelo menos um item")

        # Calcula um total simulado com base na quantidade de itens
        # Como ainda não temos tabela de produtos, usamos valor fixo por item
        valor_por_item = 15.90
        total = len(itens) * valor_por_item

        # Cria pedido
        novo_pedido = models.Pedido(
            usuario_id=usuario_id,
            canal_pedido=canal,
            status="AGUARDANDO_PAGAMENTO",
            total=total
        )

        # Salva no banco
        db.add(novo_pedido)
        db.commit()

        # Atualiza dados
        db.refresh(novo_pedido)

        return novo_pedido

    @staticmethod
    def simular_pagamento(db: Session, pedido_id: int, sucesso: bool, usuario: models.Usuario):

        # Busca pedido
        pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        # Cliente só pode pagar o próprio pedido
        # Admin pode alterar qualquer pedido
        if usuario.perfil != "ADMIN" and pedido.usuario_id != usuario.id:
            raise HTTPException(status_code=403, detail="Você não tem permissão para alterar este pedido")

        # Altera status conforme o resultado do pagamento mock
        if sucesso:
            pedido.status = "PAGO"
        else:
            pedido.status = "PAGAMENTO_RECUSADO"

        # Salva alteração
        db.commit()

        # Atualiza pedido
        db.refresh(pedido)

        return pedido

    @staticmethod
    def listar_pedidos(db: Session, usuario: models.Usuario, canal_pedido=None):

        query = db.query(models.Pedido)

        # Se não for admin, lista somente os pedidos do usuário logado
        if usuario.perfil != "ADMIN":
            query = query.filter(models.Pedido.usuario_id == usuario.id)

        # Filtro por canalPedido
        if canal_pedido:
            query = query.filter(models.Pedido.canal_pedido == canal_pedido)

        return query.all()