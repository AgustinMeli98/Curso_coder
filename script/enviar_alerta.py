import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales del correo emisor desde las variables de entorno
correo_emisor = os.getenv('CORREO_EMISOR')
password = os.getenv('CONTRASENA_EMISOR')

def enviar_correo(mensaje):
    # Configurar el servidor SMTP
    servidor_smtp = 'smtp-mail.outlook.com'  # Definir servidor de smtp
    puerto_smtp = 587

    # Configurar el mensaje de correo
    correo_destino = 'correo@destinatario.com'  # Definir correo del destinatario
    asunto = 'Alerta: Valor del dólar oficial'
    cuerpo = mensaje

    msg = MIMEText(cuerpo)
    msg['From'] = correo_emisor
    msg['To'] = correo_destino
    msg['Subject'] = asunto

    # Enviar el correo
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as server:
        server.starttls()
        server.login(correo_emisor, password)
        server.sendmail(correo_emisor, correo_destino, msg.as_string())
