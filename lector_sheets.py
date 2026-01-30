import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

def obtener_suscriptores_desde_sheets():
    # Definir el alcance de la conexión
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Lógica de credenciales para GitHub Actions o Local
    creds_json = os.getenv("GCP_SERVICE_ACCOUNT_FILE")
    
    try:
        if creds_json:
            # Si estamos en la nube (GitHub Actions)
            info = json.loads(base64.b64decode(creds_json))
            creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
        else:
            # Si estamos trabajando en Codespaces/Local
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        
        client = gspread.authorize(creds)
        
        # Conexión directa mediante tu ID proporcionado
        # El .get_worksheet(0) toma la primera pestaña de la planilla
        sheet = client.open_by_key("1uQRaU8y3JCyr67Hl4bKpNuJA7LiofAz_pBKzEae9igE").get_worksheet(0)
        
        datos = sheet.get_all_records()
        return datos

    except Exception as e:
        print(f"❌ Error en lector_sheets: {e}")
        return []