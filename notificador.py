import smtplib
import os
from email.message import EmailMessage  # <--- ESTA ES LA QUE FALTA
def enviar_email(destinatario, nombre_usuario, estrategia, analisis_ia, links_pubmed, links_lilacs):
    remitente = "marthins.mn@gmail.com" # Este podés dejarlo
    password = os.getenv("EMAIL_PASS") # Usamos variable de entorno
    # ... resto del código ...

    msg = EmailMessage()
    msg['Subject'] = f"📊 Reporte de Vigilancia: {estrategia.strip('()')}"
    msg['From'] = remitente
    msg['To'] = destinatario

    # --- DISEÑO HTML DEL MAIL ---
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
            <h2 style="color: #2c3e50;">Hola, {nombre_usuario} 👋</h2>
            <p>Este es tu reporte semanal de actualización científica generado con <b>IA</b>.</p>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 5px solid #3498db;">
                <strong>🔍 Estrategia de búsqueda:</strong><br>
                <code style="color: #e67e22;">{estrategia}</code>
            </div>

            <h3 style="color: #2980b9; margin-top: 25px;">🤖 Análisis y Priorización (IA)</h3>
            <div style="white-space: pre-wrap; background-color: #fff4e5; padding: 15px; border-radius: 5px; border: 1px solid #ffe0b2;">
                {analisis_ia}
            </div>

            <h3 style="color: #27ae60; margin-top: 25px;">📚 Evidencia Encontrada</h3>
            <p><b>PubMed:</b></p>
            <ul>
                {"".join([f'<li><a href="{l}">{l}</a></li>' for l in links_pubmed]) if links_pubmed else "<li>No se encontraron nuevos resultados.</li>"}
            </ul>

            <p><b>LILACS:</b></p>
            <ul>
                {"".join([f'<li><a href="{l}">{l}</a></li>' for l in links_lilacs]) if links_lilacs else "<li>No se encontraron nuevos resultados.</li>"}
            </ul>

            <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="font-size: 0.9em; color: #7f8c8d; text-align: center;">
                <b>BiblioBot Salud</b> - Innovación en Kinesiología Intensiva<br>
                Desarrollado por <strong>@JmNunezSilveira</strong>
            </p>
        </div>
    </body>
    </html>
    """
    
    msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(msg)
            return True
    except Exception as e:
        print(f"❌ Error de envío: {e}")
        return False
