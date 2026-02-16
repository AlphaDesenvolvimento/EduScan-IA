from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, DocumentoDB
from pydantic import BaseModel

app = FastAPI(title="EduScan AI")

# Modelo de dados para o que o usuário envia
class DocumentoSchema(BaseModel):
    titulo: str
    conteudo: str

# Função para abrir/fechar a conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/healthcheck")
def health():
    return {"status": "online"}

# --- O CRUD COMEÇA AQUI ---

# 1. Rota para SALVAR (Create)
@app.post("/documentos")
def criar_documento(doc: DocumentoSchema, db: Session = Depends(get_db)):
    novo_doc = DocumentoDB(titulo=doc.titulo, conteudo=doc.conteudo)
    db.add(novo_doc)
    db.commit()
    db.refresh(novo_doc)
    return {"mensagem": "Salvo com sucesso!", "id": novo_doc.id}

# 2. Rota para LISTAR (Read)
@app.get("/documentos")
def listar_documentos(db: Session = Depends(get_db)):
    documentos = db.query(DocumentoDB).all()
    return documentos