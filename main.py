import csv
import buscador
import buscador_lilacs
import notificador # Asegúrate de que no tenga errores de escritura
import time
def ejecutar_bot_masivo():
    print("--- 🚀 Iniciando Envío a Suscriptores ---")
    
    try:
        with open('suscriptores.csv', mode='r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            
            for persona in lector_csv:
                nombre = persona['nombre']
                email = persona['email']
                p_terms = persona['pubmed_terms']
                l_terms = persona['lilacs_terms']
                
                print(f"\n🔎 Procesando a: {nombre} ({email})")
                
                # 1. Búsquedas personalizadas
                links_p = buscador.buscar_articulos(p_terms)
                links_l = buscador_lilacs.buscar_lilacs(l_terms)
                
                # 2. Consolidar informe
                informe = [f"Hola {nombre}, aquí tienes tus novedades de la semana:\n"]
                if links_p:
                    informe.append("🔹 PUBMED:")
                    informe.extend(links_p)
                if links_l:
                    informe.append("\n🔸 LILACS:")
                    informe.extend(links_l)
                
                # 3. Enviar si hay resultados
                if links_p or links_l:
                    exito = notificador.enviar_email(email, informe)
                    if exito:
                        print(f"✅ Reporte enviado a {nombre}")
                else:
                    print(f"p Sin novedades para los términos de {nombre}")
                
                # Pausa de seguridad para no saturar los servidores (API/Email)
                time.sleep(2) 
                
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo suscriptores.csv")

if __name__ == "__main__":
    ejecutar_bot_masivo()