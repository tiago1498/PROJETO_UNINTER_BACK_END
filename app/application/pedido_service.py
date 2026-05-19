from sqlalchemy.orm import Session
from app.domain import models

# Essa classe centraliza as ações que podemos fazer com os pedidos
class PedidoService:
    @staticmethod
    def criar_novo_pedido(db: Session, usuario_id: int, canal: models.CanalPedido, itens: list):
        # Aqui a gente monta o "esqueleto" do pedido para salvar no banco
        # O valor total tá fixo só para testar, depois a gente soma os itens!
        novo_pedido = models.Pedido(
            usuario_id=usuario_id,
            canal_pedido=canal, # Garante que só aceite os canais que a gente definiu
            status="PENDENTE", # Todo pedido começa aguardando pagamento
            total=45.90 
        )
        
        db.add(novo_pedido) # Avisa o banco: "olha esse pedido novo"
        db.commit() # Salva de verdade (dá o check-in no banco)
        db.refresh(novo_pedido) # Atualiza o objeto com o ID que o banco criou
        return novo_pedido

    @staticmethod
    def simular_pagamento(db: Session, pedido_id: int, sucesso: bool):
        # Primeiro, a gente tenta achar o pedido pelo número (ID) dele
        pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
        
        # Se achou o pedido, a gente vê se o pagamento deu certo ou não
        if pedido:
            if sucesso:
                pedido.status = "PAGO"
            else:
                pedido.status = "ERRO NO PAGAMENTO"
            
            db.commit() # Salva a mudança de status
            db.refresh(pedido) # Atualiza os dados na memória
        return pedido

    @staticmethod
    def listar_todos(db: Session):
        # método para ir no banco e pega a lista de TUDO
        return db.query(models.Pedido).all()
