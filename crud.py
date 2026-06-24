from sqlalchemy.orm import Session
import models
import schemas
import hashlib

# ==========================================
# CRUD DE USUÁRIOS (Service Layer)
# ==========================================

def _criptografar_senha(senha: str) -> str:
    #Função interna para criar um hash simples da senha.
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    senha_hash = _criptografar_senha(usuario.senha)
    # Cria o modelo do banco de dados 
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def buscar_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def buscar_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def listar_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def atualizar_usuario(db: Session, usuario_id: int, dados_atualizacao: schemas.UsuarioUpdate):
    db_usuario = buscar_usuario(db, usuario_id)
    if not db_usuario:
        return None
    
    # Atualiza apenas os campos que foram enviados
    if dados_atualizacao.nome:
        db_usuario.nome = dados_atualizacao.nome
    if dados_atualizacao.email:
        db_usuario.email = dados_atualizacao.email
    if dados_atualizacao.senha:
        db_usuario.senha = _criptografar_senha(dados_atualizacao.senha)
        
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def deletar_usuario(db: Session, usuario_id: int):
    db_usuario = buscar_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False