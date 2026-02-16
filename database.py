from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Criamos o arquivo do banco local (sqlite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./eduscan.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Definimos como a tabela do EduScan será (O Modelo)
class DocumentoDB(Base):
    __tablename__ = "documentos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    conteudo = Column(String)

# 3. Criamos a tabela de fato no arquivo
Base.metadata.create_all(bind=engine)