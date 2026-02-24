from fastapi import FastAPI, Depends, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, DocumentoDB, HistoricoEstudo 
from pydantic import BaseModel
from enum import Enum
import services  # <-- MUDAMOS AQUI: Importamos o arquivo inteiro
import crud 
import prompts

# 1. Ajustado para PersonaEnum para bater com a rota
class PersonaEnum(str, Enum):
    tutor = "tutor"
    professor = "professor"
    flashcards = "flashcards"

app = FastAPI(title="EduScan AI")

# Modelo para envio manual de texto (Semana 1)
class DocumentoSchema(BaseModel):
    titulo: str
    conteudo: str

# Função de conexão com o Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/healthcheck")
def health():
    return {"status": "online"}

# --- NOVIDADE DA SEMANA 2: ROTA DE UPLOAD ---

# --- ROTA DE UPLOAD (REVISADA PARA SEMANA 3) ---

@app.post("/upload-documento")
async def upload_documento(
    arquivo: UploadFile = File(...), 
    persona: PersonaEnum = PersonaEnum.tutor,
    db: Session = Depends(get_db)
):
    conteudo_arquivo = await arquivo.read()
    
    try:
        # 1. Visão (Textract) - Extração bruta
        texto = services.extrair_texto_do_documento(conteudo_arquivo)
        
        # 2. Análise (Comprehend) - Identifica a matéria [NOVIDADE]
        materia = services.identificar_materia_documento(texto)
        
        try:
            # 3. Inteligência (Bedrock) - Resumo personalizado
            resumo = services.gerar_resumo_ai(texto, persona.value)
            
            # 4. Auditoria (CRUD) - Agora salvando a matéria também
            crud.salvar_historico(db, arquivo.filename, persona.value, texto, resumo)
            
            return {
                "status": "sucesso",
                "materia_detectada": materia,
                "resumo": resumo
            }

        except Exception as e:
            if "ThrottlingException" in str(e):
                return {
                    "status": "aviso",
                    "materia_detectada": materia,
                    "mensagem": "Cota do Bedrock atingida. Tente o resumo após as 21:00h!"
                }
            raise e

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

# --- CRUD ORIGINAL (SEMANA 1) ---

@app.post("/documentos")
def criar_documento(doc: DocumentoSchema, db: Session = Depends(get_db)):
    novo_doc = DocumentoDB(titulo=doc.titulo, conteudo=doc.conteudo)
    db.add(novo_doc)
    db.commit()
    db.refresh(novo_doc)
    return {"mensagem": "Salvo com sucesso!", "id": novo_doc.id}

@app.get("/documentos")
def listar_documentos(db: Session = Depends(get_db)):
    documentos = db.query(DocumentoDB).all()
    return documentos

# Rota para listar o historico (relatório de auditoria)
@app.get("/historico")
def listar_historico(db: Session = Depends(get_db)):
    """
    Pega todos os registros de uso da IA que foram anotados no banco de dados.
    """
    # Pedimos ao banco para buscar todos (.all) os registros da tabela HistoricoEstudo
    logs = db.query(HistoricoEstudo).all()
    return logs

@app.get("/status-quota", tags=["Monitoramento"])
def status_ia_quota():
    """
    Verifica o status atual das cotas do Amazon Bedrock sem gastar tokens significativos.
   
    """
    return services.verificar_status_ia()