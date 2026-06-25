from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from sqlalchemy.orm import Session
import crud, models, schemas, services
from database import get_db
import traceback  # <-- Adicionamos nosso radar de erros aqui

router = APIRouter(prefix="/historico", tags=["Histórico de Estudos (EduScan AI)"])

router_usuarios = APIRouter(prefix="/usuarios", tags=["Usuários"])

# 1. ROTA POST
@router.post("/upload", response_model=schemas.HistoricoEstudoResponse, status_code=status.HTTP_201_CREATED)
async def upload_documento(
    persona: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    try:
        print("\n🚀 Iniciando processamento AWS...")
        resultado_ia = await services.processar_documento_completo(file, persona)
        
        print("💾 Tentando salvar o resultado no Banco de Dados (Aiven)...")
        novo_registro = crud.salvar_historico(
            db=db,
            nome_arquivo=file.filename,
            persona=persona,
            texto_extraido=resultado_ia["texto_extraido"],
            materia_detectada=resultado_ia["materia_detectada"],
            resumo_gerado=resultado_ia["resumo_gerado"]
        )
        print("✅ Salvo com sucesso no Banco de Dados!")
        return novo_registro
    except Exception as e:
        print("\n🚨 ERRO FATAL AO SALVAR NO BANCO DE DADOS:")
        traceback.print_exc()  # <-- Isso vai forçar o erro a ficar vermelho no terminal!
        print("🚨 --------------------------------------\n")
        raise HTTPException(status_code=500, detail=f"Erro no processamento do banco: {str(e)}")

# 2. ROTA GET
@router.get("/", response_model=List[schemas.HistoricoEstudoResponse])
def listar_historicos(db: Session = Depends(get_db)):
    return crud.obter_historicos(db)

# 3. ROTA PUT
@router.put("/{historico_id}", response_model=schemas.HistoricoEstudoResponse)
def atualizar_resumo(historico_id: int, novo_resumo: str, db: Session = Depends(get_db)):
    db_historico = crud.atualizar_historico_resumo(db, historico_id, novo_resumo)
    if not db_historico:
        raise HTTPException(status_code=404, detail="Registro histórico não encontrado")
    return db_historico

# 4. ROTA DELETE
@router.delete("/{historico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_historico(historico_id: int, db: Session = Depends(get_db)):
    sucesso = crud.deletar_historico(db, historico_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Registro histórico não encontrado")
    return None

# ==========================================
# ROTAS DE USUÁRIO (Endpoints)
# ==========================================

@router_usuarios.post("/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.buscar_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.criar_usuario(db=db, usuario=usuario)

@router_usuarios.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def ler_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.buscar_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router_usuarios.put("/{usuario_id}", response_model=schemas.UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud.atualizar_usuario(db, usuario_id=usuario_id, dados_atualizacao=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router_usuarios.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    sucesso = crud.deletar_usuario(db, usuario_id=usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return None