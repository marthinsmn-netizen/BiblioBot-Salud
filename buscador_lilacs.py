import requests
import datetime

def buscar_lilacs(terminos, dias_atras=7):
    # LILACS usa un formato de fecha distinto
    fecha_corte = (datetime.datetime.now() - datetime.timedelta(days=dias_atras)).strftime("%Y%m%d")
    
    # URL de la API de la BVS / LILACS
    url = "https://pesquisa.bvsalud.org/portal/backend/search"
    
    params = {
        "q": terminos,
        "filter[entry_date][]": f"[{fecha_corte} TO 30001231]",
        "output": "json",
        "lang": "es"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extraemos los links de los documentos encontrados
        docs = data.get("response", {}).get("docs", [])
        links = []
        for doc in docs:
            # Construimos el link directo usando el ID de la BVS
            id_doc = doc.get("id")
            links.append(f"https://pesquisa.bvsalud.org/portal/resource/es/{id_doc}")
        
        return links
    except Exception as e:
        print(f"Error en LILACS: {e}")
        return []