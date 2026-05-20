from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.domain import models

# Configuração do jwt
SECRET_KEY = "123456"
ALGORITHM = "HS256" 
# criptografia da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# rota do login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#  FUNÇÕES DE SENHA 

def gerar_senha_hash(senha):
    return pwd_context.hash(senha)

# verifica senha
def verificar_senha(senha_pura, senha_hash):
    return pwd_context.verify(senha_pura, senha_hash)

#  FUNÇÕES DE TOKEN 

# # Cria token jwt
def criar_token_acesso(dados: dict):
    expira = datetime.utcnow() + timedelta(minutes=30)
    dados_copia = dados.copy()
    # tempo de expiração
    dados_copia.update({"exp": expira}) 
    return jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

# FUNÇÃO DE VALIDAÇÃO

# Autentica usuário
def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Erro de autenticação
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # Pega o e-mail do token
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    #Busca usuario no banco
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario 
