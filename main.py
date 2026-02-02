import buscador
import buscador_lilacs
import notificador
import lector_sheets
import analizador
import time
import os

def ejecutar_bot_masivo():
    print("--- 🚀 Iniciando BiblioBot Pro con IA ---")
    print("--- 💡 Innovación por @JmNunezSilveira ---\n")
    
    try:
        # 1. Obtener datos desde Google Sheets
        # Asegúrate de que las columnas en Sheets coincidan (Nombre, Email, Pubmed_Terms, etc.)
        suscriptores = lector_sheets.obtener_suscriptores_desde_sheets()
        
        if not suscriptores:
            print("⚠️ No se encontraron suscriptores en la hoja.")
            return

        print(f"📊 Se encontraron {len(suscriptores)} suscriptores. Iniciando proceso...")

        for persona in suscriptores:
            # Normalizar nombres de columnas a minúsculas y sin espacios
            p_lower = {k.lower().strip(): v for k, v in persona.items()}
            
            nombre = p_lower.get('nombre', 'Colega')
            email = p_lower.get('email') or p_lower.get('dirección de correo electrónico')
            p_terms = p_lower.get('pubmed_terms') or p_lower.get('keywords pubmed') or ""
            l_terms = p_lower.get('lilacs_terms') or p_lower.get('keywords lilacs') or ""
            filtros = p_lower.get('filtros_extra') or p_lower.get('filtros') or ""
            
            if not email:
                print(f"⏭️ Saltando a {nombre} porque no tiene email.")
                continue

            print(f"\n🔎 Procesando: {nombre} ({email})")
            
            # 2. Búsquedas en bases de datos
            # buscador.buscar_articulos devuelve (lista_links, estrategia_usada)
            links_p, estrategia_p = buscador.buscar_articulos(p_terms, filtros)
            links_l = buscador_lilacs.buscar_lilacs(l_terms)
            
            # 3. Análisis de IA (Usando el motor de Groq en analizador.py)
            analisis_ia = ""
            if links_p:
                print("🤖 Consultando a la IA para analizar evidencia...")
                analisis_ia = analizador.categorizar_estudios(links_p)
            else:
                print("⌛ No se encontraron papers en PubMed para analizar.")

            # 4. Envío del email con formato HTML profesional
            if links_p or links_l:
                print(f"📧 Enviando reporte a {email}...")
                exito = notificador.enviar_email(
                    destinatario=email,
                    nombre_usuario=nombre,
                    estrategia=estrategia_p if estrategia_p else p_terms,
                    analisis_ia=analisis_ia,
                    links_pubmed=links_p,
                    links_lilacs=links_l
                )
                
                if exito:
                    print(f"✅ Reporte enviado con éxito a {nombre}")
                    # 5. Pausa de seguridad para evitar bloqueos de Gmail/IA
                    print("⏳ Esperando 10 segundos para el próximo envío...")
                    time.sleep(10)
                else:
                    print(f"❌ Falló el envío del mail a {nombre}")
            else:
                print(f"🤷 Sin novedades esta semana para los términos de {nombre}.")
        
        print("\n--- ✅ Proceso masivo finalizado con éxito ---")
                
    except Exception as e:
        print(f"❌ Error crítico en el flujo principal: {e}")

if __name__ == "__main__":
    ejecutar_bot_masivo()