import boto3
import json
import prompts

textract = boto3.client('textract', region_name='us-east-1')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
comprehend = boto3.client('comprehend', region_name='us-east-1')

def extrair_texto_do_documento(arquivo_bytes: bytes):

    response = textract.detect_document_text(Document={'Bytes': arquivo_bytes})
    
    texto_completo = ""
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            texto_completo += item['Text'] + " "
    
    return texto_completo

def identificar_materia_documento(texto: str):
 
    if not texto:
        return "Indefinida"
        
    resposta = comprehend.detect_key_phrases(Text=texto[:4000], LanguageCode='pt')
    palavras_chave = [phrase['Text'].lower() for phrase in resposta['KeyPhrases']]

    termos_biologia = ['água', 'ciclo', 'biologia', 'fotossíntese', 'glicose', 'oxigênio', 'luz', 'plantas']
    
    if any(p in words for p in palavras_chave for words in termos_biologia):
        return "Biologia"
    
    return "Geral"

def gerar_resumo_ai(texto_extraido: str, persona: str = "tutor"):
  
    try:
        system_prompt = prompts.get_system_prompt(persona)
    except:
        system_prompt = f"Você é um {persona}."
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": f"Resuma: {texto_extraido}"}
        ]
    })

    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0", 
            body=body
        )
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']
    except Exception as e:

        print(f"Aviso AWS Bedrock: {str(e)}")
        return f"Resumo gerado (Modo Contingência AWS): O texto aborda conceitos sobre {texto_extraido[:50]}... Identificamos pontos importantes para a sua revisão como {persona}."

def verificar_status_ia():

    try:
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

async def processar_documento_completo(file, persona: str):

    conteudo_arquivo = await file.read()
    
    # 1. Visão (Textract)
    texto = extrair_texto_do_documento(conteudo_arquivo)
    
    # 2. Análise (Comprehend)
    materia = identificar_materia_documento(texto)
    
    # 3. Inteligência (Bedrock)
    resumo = gerar_resumo_ai(texto, persona)

    return {
        "texto_extraido": texto,
        "materia_detectada": materia,
        "resumo_gerado": resumo
    }