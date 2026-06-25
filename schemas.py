from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# ==========================================
# SCHEMAS DE HISTÓRICO DE ESTUDOS (EduScan)
# ==========================================

class HistoricoEstudoResponse(BaseModel):
    id: int
    texto_extraido: str
    materia_detectada: str
    resumo_gerado: str
    # data_criacao: datetime  (se houver, pode deixar)

    class Config:
        from_attributes = True


# ==========================================
# SCHEMAS DE USUÁRIO
# ==========================================

class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    email: EmailStr 

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6, description="Senha com no mínimo 6 caracteres")

class UsuarioResponse(UsuarioBase):
    id: int
    data_cadastro: datetime

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=6)