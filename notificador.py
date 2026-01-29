def enviar_email(destinatario, links):
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    msg = EmailMessage()
    msg['Subject'] = "📚 Alerta Bibliográfica | BiblioBot Salud"
    msg['From'] = f"BiblioBot Salud <{user}>"
    msg['To'] = destinatario

    # Construimos el cuerpo del mensaje en HTML
    items_html = ""
    for link in links:
        if "---" in link or "NUEVOS" in link:
            items_html += f"<li style='list-style:none; margin-top:15px; font-weight:bold; color:#0d6efd;'>{link}</li>"
        else:
            items_html += f"<li style='margin-bottom:10px;'><a href='{link}' style='color:#0d6efd; text-decoration:none;'>🔗 Ver publicación en el sitio oficial</a></li>"

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden;">
                <div style="background-color: #0d6efd; color: white; padding: 20px; text-align: center;">
                    <h1 style="margin:0;">BiblioBot Salud</h1>
                    <p style="margin:0;">Tu vigilancia científica semanal</p>
                </div>
                <div style="padding: 20px;">
                    <p>Hola,</p>
                    <p>He analizado las últimas publicaciones en <strong>PubMed</strong> y <strong>LILACS</strong> según tus intereses. Aquí tienes los hallazgos de esta semana:</p>
                    <ul style="padding-left: 0;">
                        {items_html}
                    </ul>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="font-size: 12px; color: #777; text-align: center;">
                        Este es un servicio automatizado creado por el Lic. J.M. Nuñez Silveira.<br>
                        Para modificar tus keywords, responde a este correo.
                    </p>
                </div>
            </div>
        </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error de envío: {e}")
        return False