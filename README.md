# EduScan AI 🎓🤖

O **EduScan AI** é uma solução de software robusta e de nível de produção desenvolvida para otimizar a rotina de estudos através da digitalização e sumarização inteligente de anotações físicas. A aplicação adota uma arquitetura em camadas de alto desempenho, integrando serviços de inteligência artificial da **AWS** a um banco de dados relacional totalmente gerenciado na nuvem.

---

## 🚀 Status e Evolução do Projeto

**📅 Semana 1 a 3: Fundação, Visão e Inteligência Artificial (Concluídas ✅)**
* **Core API:** Implementação de rotas assíncronas com FastAPI e orquestração do pipeline de processamento.
* **AWS Textract (Visão Computacional):** OCR avançado para extração real de textos a partir de fotos de cadernos.
* **AWS Comprehend (NLP):** Processamento de Linguagem Natural para classificação automática da matéria estudada.
* **Amazon Bedrock (Generative AI):** Engenharia de prompt utilizando o modelo Claude Haiku para gerar resumos adaptados à persona didática selecionada.
* **Resiliência:** Tratamento de exceções para limites de taxa (Throttling) da nuvem e monitoramento de cota.

**📅 Semana 4: Segurança, Governança e Banco de Dados Remoto (Concluída ✅)**
* **Arquitetura Enterprise:** Divisão rigorosa de responsabilidades através do padrão **Models, Schemas, CRUD/Services e Views**.
* **Gestão de Usuários:** Sistema completo de cadastro e gerenciamento com endpoints totalmente testados.
* **Criptografia e Proteção:** Implementação de hash criptográfico **SHA-256** para tratamento seguro de credenciais.
* **Migração de Dados (Cloud DB):** Substituição do banco local (SQLite) por uma instância em nuvem do **PostgreSQL** totalmente gerenciada na **Aiven**.

---

## 🏗️ Padrão de Arquitetura do Sistema

A API foi projetada seguindo o princípio da **Separação de Conceitos (SoC)**, dividindo-se nas seguintes camadas:

* **Camada de Model (`models.py`):** Define a estrutura física das tabelas de Histórico e Usuários utilizando o SQLAlchemy ORM.
* **Camada de Schema (`schemas.py`):** Controla a validação estrutural de entrada e saída de dados com Pydantic, mascarando dados confidenciais.
* **Camada de Service/CRUD (`crud.py`):** Centraliza as regras de negócio e consultas ao banco de dados, incluindo o mascaramento criptográfico de senhas.
* **Camada de View (`views.py`):** Expõe os endpoints de forma organizada utilizando roteadores independentes (`APIRouter`) para isolamento de escopo.

---

## 🛠️ Tech Stack

* **Linguagem:** Python 3.13
* **Framework:** FastAPI (Assíncrono)
* **Banco de Dados:** PostgreSQL (Instância de Produção Nuvem gerenciada na **Aiven**)
* **Mapeamento Relacional:** SQLAlchemy
* **Validação e Tipagem:** Pydantic (com `email-validator`)
* **Servidor ASGI:** Uvicorn
* **SDK Cloud:** Boto3 (AWS SDK)
* **Soluções de IA (AWS Cloud):**
    * Amazon Textract (Extração de Texto/OCR)
    * Amazon Comprehend (Classificação de Texto/NLP)
    * Amazon Bedrock - Claude Haiku (IA Generativa/LLM)

---

## 🔐 Segurança e Governança de Dados

* **Princípio do Menor Privilégio (IAM):** Permissões estritas aplicadas às credenciais de execução da API na AWS.
* **Segurança de Payloads:** Os dados de tráfego omitiram campos confidenciais (ex: senhas não trafegam nos retornos de requisição HTTP).
* **Proteção Criptográfica:** Uso de algoritmo hash SHA-256 nativo para evitar o armazenamento de senhas em formato textual puro.
* **Push Protection:** Segurança de chaves ativada no repositório para evitar vazamento acidental de credenciais em ambiente público.

---

## 🛣️ Dicionário de Endpoints (Rotas da API)

### 📚 Módulo: Histórico de Estudos (`/historico`)

| Método | Rota | Descrição | Status |
| :--- | :--- | :--- | :--- |
| `POST` | `/historico/upload` | Pipeline completo: Imagem -> OCR -> NLP -> Resumo GenAI. | ✅ Concluído |
| `GET` | `/historico/` | Lista o histórico completo de resumos gerados. | ✅ Concluído |
| `PUT` | `/historico/{id}` | Atualiza o conteúdo textual de um resumo específico. | ✅ Concluído |
| `DELETE` | `/historico/{id}` | Remove permanentemente um log do banco de dados. | ✅ Concluído |

### 👥 Módulo: Usuários (`/usuarios`)

| Método | Rota | Descrição | Status |
| :--- | :--- | :--- | :--- |
| `POST` | `/usuarios/` | Cadastro de usuário com geração automática de hash de segurança. | ✅ Concluído |
| `GET` | `/usuarios/{id}` | Recupera os dados cadastrais públicos do usuário. | ✅ Concluído |
| `PUT` | `/usuarios/{id}` | Atualização dinâmica de informações de perfil. | ✅ Concluído |
| `DELETE` | `/usuarios/{id}` | Exclusão de registro cadastral do banco em nuvem. | ✅ Concluído |

### 🖥️ Módulo: Monitoramento de Sistema

| Método | Rota | Descrição | Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/healthcheck` | Verifica a integridade e disponibilidade da API. | ✅ Concluído |
| `GET` | `/status-quota` | Auditoria interna de tokens e cotas de uso da AWS. | ✅ Concluído |

---

## 📦 Como rodar o projeto localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/AlphaDesenvolvimento/EduScan-IA.git](https://github.com/AlphaDesenvolvimento/EduScan-IA.git)
   cd EduScan-IA

1. **Ative o ambiente virtual:**
   ```powershell
   .\venv\Scripts\activate

2. **Instale as dependências diretamente através do interpretador:**
   ```powershell
   python -m pip install fastapi uvicorn sqlalchemy python-multipart boto3 pydantic[email] email-validator psycopg2-binary

3. **Inicie o servidor Uvicorn de forma isolada:**
   ```powershell
   python -m uvicorn main:app --reload

4. **Acesse a documentação interativa:**
   Abra o navegador em http://127.0.0.1:8000/docs para interagir e testar as operações em tempo real através do Swagger UI.
