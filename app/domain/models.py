from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

# criado para limitar as opcoes do canal de venda
# para evitar que as pessoas mandassem qualquer coisa no postman
class CanalPedido(enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    perfil = Column(String, default="CLIENTE")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    canal_pedido = Column(Enum(CanalPedido), nullable=False) 
    status = Column(String, default="AGUARDANDO PAGAMENTO") 
    total = Column(Float)
