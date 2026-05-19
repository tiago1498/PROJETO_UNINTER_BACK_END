from sqlalchemy.orm import Session
from app.domain import models
from app.infrastructure import security

class AuthService:
    @staticmethod
    def autenticar_usuario(db: Session, email: str, senha_pura: str):
        usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
        if not usuario:
            return False
        if not security.verificar_senha(senha_pura, usuario.senha_hash):
            return False
        return usuario
