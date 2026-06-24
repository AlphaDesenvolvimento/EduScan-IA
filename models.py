from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# --- Histórico de estudos ---
class HistoricoEstudo(Base):
    __tablename__ = "historicos_estudos"

    id = Column(Integer, primary_key=True, index=True)
    materia_detectada = Column(String, index=True)
    texto_extraido = Column(String)
    resumo_gerado = Column(String)
    data_criacao = Column(DateTime, default=datetime.utcnow)


# --- CAMADA DE MODEL USUÁRIO ---
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False) # Guardará o hash da senha
    data_cadastro = Column(DateTime, default=datetime.utcnow)