import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

def test():
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    print(f"Probando envío desde: {user}")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(user, password)
            server.sendmail(user, user, "Subject: Test BiblioBot\n\nEste es un test de conexion.")
        print("✅ ¡CONEXIÓN EXITOSA! El problema de la contraseña se resolvió.")
    except Exception as e:
        print(f"❌ Error todavía presente: {e}")

if __name__ == "__main__":
    test()