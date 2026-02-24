# EduScan AI 🎓🤖

**EduScan AI** é uma API inteligente desenvolvida para otimizar a rotina de estudos através da sumarização automática de documentos educacionais. O projeto utiliza Python e FastAPI integrados a serviços avançados de Inteligência Artificial da AWS.

## 🚀 Status do Projeto

**📅 Semana 1: A Fundação (Concluída ✅)**
- [x] Configuração de ambiente virtual (venv).
- [x] Implementação de rotas básicas com FastAPI.
- [x] Integração de banco de dados SQL (SQLite/SQLAlchemy) para persistência inicial.

**📅 Semana 2: O Cérebro da IA (Concluída ✅)**
- [x] Implementação de suporte a upload de arquivos (Imagens e PDFs).
- [x] Criação da camada de serviços (services.py) para processamento de IA.
- [x] Integração automática: Upload -> Extração -> Resumo -> Banco de Dados.

**📅 Semana 3: Visão e Auditoria (Concluída ✅)**
[x] OCR Avançado: Extração real de textos a partir de fotos de cadernos via Textract.
[x] Classificação Inteligente: Integração com Amazon Comprehend para identificação automática da matéria (NLP).
[x] Resiliência e Monitoramento: Implementação de tratamento de erros para cotas de API (Throttling) e rota de status de saúde da IA.
[x] Segurança IAM: Configuração de políticas de acesso granular para o usuário da aplicação.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.13
- **Framework:** FastAPI
- **Servidor:** Uvicorn
- **SDK AWS:** Boto3
- **Banco de Dados:** SQLite com SQLAlchemy (Audit Log).
- **IA & Cloud:** Amazon Textract (IA Preditiva/OCR), Amazon Comprehend (NLP) e Amazon Bedrock (IA Generativa/LLMs).

## 📦 Como rodar o projeto localmente

1. **Ative o ambiente virtual:**
   ```powershell
   .\venv\Scripts\activate

2. **Instale as dependências:**
   ```powershell
   python -m pip install fastapi uvicorn sqlalchemy python-multipart boto3

3. **Inicie o servidor (Evitando erro de launcher):**
   ```powershell
   python -m uvicorn main:app --reload

4. **Acesse a documentação interativa:**
   Vá para http://127.0.0.1:8000/docs para testar o upload de arquivos.

## 🛣️ Endpoints Disponíveis

| Método | Rota | Descrição | Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/healthcheck` | Verifica se a API está online. | ✅ Pronto |
| `POST` | `/upload-documento` | Processa imagem -> OCR -> Classificação -> Resumo. | ✅ Pronto |
| `GET` | `/documentos` | Lista todos os resumos e textos salvos no banco de dados. | ✅ Pronto |
| `POST` | `/documentos` | Permite a criação manual de um registro de documento (Semana 1). | ✅ Pronto |
| `GET` | `/historico` | Lista o log de auditoria com textos extraídos e resumos gerados. | ✅ Pronto |
| `GET` | `/status-quota` | Verifica a disponibilidade de tokens na AWS Bedrock. | ✅ Pronto |

## ☁️ Conexão com a Certificação (AWS Certified AI Practitioner)

Este projeto aplica conceitos fundamentais da certificação AWS:

1. IA Preditiva vs. Generativa: Uso do Textract para predição de texto (OCR) e Bedrock para geração de conteúdo (GenAI).
2. Segurança (IAM): Implementação do Princípio do Menor Privilégio, garantindo que a aplicação acesse apenas os serviços necessários (ComprehendFullAccess, TextractFullAccess).
3. Governança de Custos: Monitoramento de Service Quotas e tratamento de exceções de Throttling para evitar estouro de limites diários.