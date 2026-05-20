from sqlalchemy.orm import Session
from app.domain import models

# serviço de pedidos
class PedidoService:

    @staticmethod
    def criar_novo_pedido(db: Session, usuario_id: int, canal: models.CanalPedido, itens: list):
        
        # cria pedido
        novo_pedido = models.Pedido(
            usuario_id=usuario_id,
            canal_pedido=canal,
            status="PENDENTE",
            total=45.90
        )

        # salva no banco
        db.add(novo_pedido)
        db.commit()

        # atualiza dados
        db.refresh(novo_pedido)

        return novo_pedido

    @staticmethod
    def simular_pagamento(db: Session, pedido_id: int, sucesso: bool):

        # busca pedido
        pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

        # altera status
        if pedido:
            if sucesso:
                pedido.status = "PAGO"
            else:
                pedido.status = "ERRO NO PAGAMENTO"

            # salva alteração
            db.commit()

            # atualiza pedido
            db.refresh(pedido)

        return pedido

    @staticmethod
    def listar_todos(db: Session):

        # lista pedidos
        return db.query(models.Pedido).all()