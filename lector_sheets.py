import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def obtener_suscriptores_desde_sheets():
    # Definimos los permisos necesarios
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        # 1. Intentamos obtener las credenciales desde la variable de entorno (GitHub Secrets)
        creds_json = os.getenv("GCP_SERVICE_ACCOUNT_FILE")
        
        if creds_json:
            print("🔐 Autenticando mediante Secret de GitHub...")
            # Cargamos el JSON directamente desde el texto del Secret
            info = json.loads(creds_json)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
        
        # 2. Si no hay Secret, buscamos el archivo físico (Entorno local/Codespace)
        elif os.path.exists("credentials.json"):
            print("🏠 Autenticando mediante archivo local credentials.json...")
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        
        else:
            print("❌ ERROR: No se encontró ni el Secret GCP_SERVICE_ACCOUNT_FILE ni el archivo credentials.json")
            return []

        # Autorizamos el cliente
        client = gspread.authorize(creds)
        
        # 3. Abrimos la hoja de cálculo
        # IMPORTANTE: Asegúrate de que el nombre "BiblioBot" sea idéntico al de tu archivo en Google Drive
        nombre_hoja = "BiblioBot" 
        sheet = client.open(nombre_hoja).get_worksheet(0)
        
        # Obtenemos todos los registros
        datos = sheet.get_all_records()
        print(f"📊 Datos recuperados: {len(datos)} suscriptores encontrados.")
        return datos

    except Exception as e:
        print(f"❌ Error crítico en lector_sheets: {e}")
        return []
