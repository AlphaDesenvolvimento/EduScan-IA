import boto3
import json
import prompts

# Inicialização dos Clientes (Agora com sinal verde!)
textract = boto3.client('textract', region_name='us-east-1')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
comprehend = boto3.client('comprehend', region_name='us-east-1')

def extrair_texto_do_documento(arquivo_bytes: bytes):
    """
    Usa o Amazon Textract para extrair texto real.
    """
    response = textract.detect_document_text(Document={'Bytes': arquivo_bytes})
    
    texto_completo = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            texto_completo += item['Text'] + " "
    
    return texto_completo

def gerar_resumo_ai(texto_extraido: str, persona: str = "tutor"):
    """
    Usa o Claude 3 no Bedrock para processar o texto extraído.
    """
    system_prompt = prompts.get_system_prompt(persona)
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": f"Resuma este conteúdo: {texto_extraido}"}
        ],
        "temperature": 0.5
    })

    # Usando o perfil de inferência global para evitar erros de cota
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0", 
        body=body
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def verificar_status_ia():
    """
    Realiza um teste rápido (ping) para verificar se a cota diária foi resetada.
   
    """
    try:
        # Enviamos apenas 1 token para não gastar sua cota real
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "ping"}]
        })
        
        bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0", 
            body=body
        )
        return {"disponivel": True, "mensagem": "🚀 IA Pronta! Cota liberada pela AWS."}
        
    except Exception as e:
        if "ThrottlingException" in str(e):
            return {
                "disponivel": False, 
                "mensagem": "⏳ Limite diário ainda ativo. Tente após as 21:00h."
            }
        return {"disponivel": False, "mensagem": f"⚠️ Outro erro: {str(e)}"}
    
def identificar_materia_documento(texto: str):
    # Usa Processamento de Linguagem Natural (NLP) para identificar o tema.

    if not texto:
        return "Indefinida"
        
    # Analisamos as frases-chave do documento
    resposta = comprehend.detect_key_phrases(Text=texto[:4000], LanguageCode='pt')
    
    # Lógica simples: se houver 'água' ou 'evaporação', sugerimos Biologia/Ciências
    palavras_chave = [phrase['Text'].lower() for phrase in resposta['KeyPhrases']]
    
    if any(p in words for p in palavras_chave for words in ['água', 'ciclo', 'biologia']):
        return "Ciências/Biologia"
    
    return "Geral"