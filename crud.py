from sqlalchemy.orm import Session
from database import HistoricoEstudo # Importando o modelo que define a "Tabela 2"

def salvar_historico(db: Session, arquivo_nome: str, persona: str, texto: str, resumo: str):
    """
    Função responsável por criar um novo registro na tabela de histórico de estudos.
    """
    novo_registro = HistoricoEstudo(
        arquivo_nome=arquivo_nome,
        persona=persona,
        texto_extraido=texto,
        resumo_ia=resumo
    )
    db.add(novo_registro)      # Adiciona o objeto à sessão do banco
    db.commit()                # Salva as alterações permanentemente
    db.refresh(novo_registro)  # Atualiza o objeto com os dados do banco (como o ID)
    return novo_registro