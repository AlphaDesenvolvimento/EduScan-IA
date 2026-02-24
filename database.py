from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuração do SQLite (Seu banco local atual)
SQLALCHEMY_DATABASE_URL = "sqlite:///./eduscan.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definimos a Base apenas UMA vez aqui
Base = declarative_base()

# Tabela da Semana 1: Guarda o Título e o Conteúdo manual
class DocumentoDB(Base):
    __tablename__ = "documentos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    conteudo = Column(String)

# --- NOVIDADE: Tabela de Histórico (Simulando a estrutura do DynamoDB) ---
class HistoricoEstudo(Base):
    __tablename__ = "historico_estudos"

    id = Column(Integer, primary_key=True, index=True)
    arquivo_nome = Column(String)
    persona = Column(String)          # Tutor, Professor ou Flashcards
    texto_extraido = Column(Text)     # O que o Textract leu
    resumo_ia = Column(Text)          # O que o Bedrock gerou
    data_criacao = Column(DateTime, default=datetime.utcnow)

# Cria as tabelas no arquivo .db automaticamente
Base.metadata.create_all(bind=engine)