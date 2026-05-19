from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.domain import models

# Configurações que não podem vazar! A SECRET_KEY é tipo a senha do servidor
SECRET_KEY = "sua_chave_secreta_muito_segura" 
ALGORITHM = "HS256" # O "estilo" de criptografia que vamos usar
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Avisa ao FastAPI que o token vai vir lá do endpoint "login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- FUNÇÕES DE SENHA ---

# Transforma a senha "123456" em uma zona tipo "$2b$12$..." pra ninguém ler
def gerar_senha_hash(senha):
    return pwd_context.hash(senha)

# Compara a senha que o usuário digitou com a que está salva no banco
def verificar_senha(senha_pura, senha_hash):
    return pwd_context.verify(senha_pura, senha_hash)

# --- FUNÇÕES DE TOKEN ---

# Cria o "ticket" de entrada do usuário que vale por 30 minutos
def criar_token_acesso(dados: dict):
    expira = datetime.utcnow() + timedelta(minutes=30)
    dados_copia = dados.copy()
    dados_copia.update({"exp": expira}) # Coloca a data de validade dentro do token
    return jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

# --- FUNÇÃO DE VALIDAÇÃO ---

# Essa função é a que protege as outras rotas
def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Mensagem padrão de erro se algo der errado no login
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Tenta abrir o token usando a nossa chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # Pega o e-mail que guardamos lá dentro
        if email is None:
            raise credentials_exception
    except JWTError:
        # Se o token estiver vencido ou for falso, cai aqui
        raise credentials_exception

    # Vai no banco de dados e procura o dono desse e-mail
    # Importante: retorna o OBJETO (com id, nome, etc) e não só o texto do e-mail
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario # Pronto, o usuário está autenticado e pode seguir!
