from fastapi import FastAPI
from app.api import pedido_routes
from app.infrastructure.database import engine
from app.domain.models import Base
from app.api import auth_routes

# comando pra criar as tabelas no banco de dados automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rede Raízes do Nordeste")

# Registra as rotas de pedidos
app.include_router(pedido_routes.router, tags=["Pedidos"])
app.include_router(auth_routes.router, tags=["Segurança"])

@app.get("/")
def root():
    return {"status": "Sistema Online"}
