import requests
import json

def categorizar_estudios(links):
    # --- PEGA ACÁ TU NUEVA CLAVE DE GROQ ---
    api_key = "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"
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = f"""
    Actúa como un experto en Kinesiología Intensiva. 
    Analiza estos links de PubMed: {links}.
    Para cada uno, indica:
    1. PRIORIDAD (Alta, Media, Baja).
    2. Una breve sugerencia clínica de 1 oración.
    Responde en español de forma profesional.
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        
        if "choices" in res_json:
            return res_json['choices'][0]['message']['content']
        else:
            return f"⚠️ Error en Groq: {res_json.get('error', {}).get('message', 'Error desconocido')}"

    except Exception as e:
        return f"⚠️ Error de conexión: {e}"