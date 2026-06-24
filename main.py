from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from database import engine
import services
import views
import models

# Cria as tabelas novas no banco de dados assim que o servidor liga
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduScan AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(views.router)
app.include_router(views.router_usuarios)

@app.get("/healthcheck", tags=["Monitoramento"])
def health():
    return {"status": "online"}

@app.get("/status-quota", tags=["Monitoramento"])
def status_ia_quota():
    
    #Verifica o status atual das cotas do Amazon Bedrock.

    return services.verificar_status_ia()