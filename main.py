import buscador
import buscador_lilacs
import notificador
import lector_sheets
import time

def ejecutar_bot_masivo():
    print("--- 🚀 Iniciando Envío desde Google Sheets ---")
    
    try:
        suscriptores = lector_sheets.obtener_suscriptores_desde_sheets()
        
        if not suscriptores:
            print("⚠️ No se encontraron suscriptores en la hoja.")
            return

        for persona in suscriptores:
            # Normalizamos las llaves a minúsculas para evitar errores de tipeo en el Sheet
            p_lower = {k.lower().strip(): v for k, v in persona.items()}
            
            nombre = p_lower.get('nombre') or p_lower.get('nombre y apellido') or "Colega"
            email = p_lower.get('email') or p_lower.get('dirección de correo electrónico')
            p_terms = p_lower.get('pubmed_terms') or p_lower.get('keywords pubmed') or ""
            l_terms = p_lower.get('lilacs_terms') or p_lower.get('keywords lilacs') or ""
            
            if not email:
                continue

            print(f"\n🔎 Procesando a: {nombre} ({email})")
            
            # 1. Búsquedas
            links_p = buscador.buscar_articulos(p_terms)
            links_l = buscador_lilacs.buscar_lilacs(l_terms)
            
            # 2. Consolidar informe
            informe = []
            if links_p:
                informe.append("--- RESULTADOS DE PUBMED ---")
                informe.extend(links_p)
            if links_l:
                informe.append("--- RESULTADOS DE LILACS ---")
                informe.extend(links_l)
            
            # 3. Enviar si hay resultados
            if links_p or links_l:
                exito = notificador.enviar_email(email, informe)
                if exito:
                    print(f"✅ Reporte enviado a {nombre}")
            else:
                print(f"⌛ Sin novedades para: {nombre}")
            
            time.sleep(2) 
                
    except Exception as e:
        print(f"❌ Error en la ejecución: {e}")

if __name__ == "__main__":
    ejecutar_bot_masivo()