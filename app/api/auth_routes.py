from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure import security
from app.application.auth_service import AuthService
from app.domain import models
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Rota de cadastro
@router.post("/cadastro")
def cadastrar(nome: str, email: str, senha: str, db: Session = Depends(get_db)):
    hash_da_senha = security.gerar_senha_hash(senha)
    
    # Cria usuário 
    novo_usuario = models.Usuario(nome=nome, email=email, senha_hash=hash_da_senha, perfil="CLIENTE")
    
    # Salva no banco
    db.add(novo_usuario)
    db.commit()
    
    return {"mensagem": "Usuário criado com sucesso"}

# Rota de login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    #autentica usuário
    usuario = AuthService.autenticar_usuario(db, form_data.username, form_data.password)
    
    #Verifica login
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    
    # Gera toke jwt
    token = security.criar_token_acesso({"sub": usuario.email, "perfil": usuario.perfil})
    return {"access_token": token, "token_type": "bearer"}

