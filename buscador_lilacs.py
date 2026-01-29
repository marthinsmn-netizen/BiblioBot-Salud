import requests
import datetime

def buscar_lilacs(terminos, dias_atras=7):
    fecha_corte = (datetime.datetime.now() - datetime.timedelta(days=dias_atras)).strftime("%Y%m%d")
    url = "https://pesquisa.bvsalud.org/portal/backend/search"
    params = {
        "q": terminos,
        "filter[entry_date][]": f"[{fecha_corte} TO 30001231]",
        "output": "json",
        "lang": "es"
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            docs = data.get("response", {}).get("docs", [])
            return [f"https://pesquisa.bvsalud.org/portal/resource/es/{d.get('id')}" for d in docs if d.get('id')]
        return []
    except Exception:
        return []
