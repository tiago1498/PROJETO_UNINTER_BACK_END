from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure import security
from app.application.auth_service import AuthService
from app.domain import models
from fastapi.security import OAuth2PasswordRequestForm
from app.api import schemas

router = APIRouter()

# Rota de cadastro
@router.post("/cadastro")
def cadastrar(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()

    if usuario_existente:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")

    hash_da_senha = security.gerar_senha_hash(dados.senha)

    novo_usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_da_senha,
        perfil=dados.perfil
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "mensagem": "Usuário criado com sucesso",
        "usuario": {
            "id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "email": novo_usuario.email,
            "perfil": novo_usuario.perfil
        }
    }

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

