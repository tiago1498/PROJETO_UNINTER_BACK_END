from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure import security
from app.application.auth_service import AuthService
from app.domain import models
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Rota para criar uma conta nova
@router.post("/cadastro")
def cadastrar(nome: str, email: str, senha: str, db: Session = Depends(get_db)):
    # Importante: nunca salvar a senha pura! Esse comando transforma a senha em um código (hash)
    hash_da_senha = security.gerar_senha_hash(senha)
    
    # Preenche a ficha do novo usuário com os dados recebidos
    novo_usuario = models.Usuario(nome=nome, email=email, senha_hash=hash_da_senha, perfil="CLIENTE")
    
    # Comandos do banco: adiciona na fila e depois confirma (commit) para salvar de verdade
    db.add(novo_usuario)
    db.commit()
    
    return {"mensagem": "Usuário criado com sucesso (LGPD: Dados criptografados)"}

# Rota para entrar no sistema (Login)
@router.post("/login")
# Esse 'OAuth2PasswordRequestForm' faz aparecer aqueles campos de login  no Swagger (documentação)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Chama o serviço de autenticação para ver se o e-mail e a senha batem
    # Obs: O FastAPI chama o e-mail de 'username' por padrão nesse formulário
    usuario = AuthService.autenticar_usuario(db, form_data.username, form_data.password)
    
    # Se o serviço não encontrar o usuário ou a senha estiver errada, trava aqui
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    
    # Se deu tudo certo, cria o crachá digital (token) para o usuário usar nas outras rotas
    token = security.criar_token_acesso({"sub": usuario.email, "perfil": usuario.perfil})
    
    # Devolve o token pro navegador/celular guardar
    return {"access_token": token, "token_type": "bearer"}

