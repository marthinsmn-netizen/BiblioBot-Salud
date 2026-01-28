import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def enviar_email(destinatario, links):
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    msg = EmailMessage()
    msg['Subject'] = "📚 BiblioBot: Novedades Científicas"
    msg['From'] = user
    msg['To'] = destinatario
    cuerpo = "Hola,\n\nHe encontrado estos artículos para ti:\n\n" + "\n".join(links)
    msg.set_content(cuerpo)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error de envío: {e}")
        return False
