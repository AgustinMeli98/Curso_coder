from datetime import datetime
import os
from dotenv import load_dotenv
import requests
from sqlalchemy import create_engine, Column, String, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import smtplib
from email.mime.text import MIMEText

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales de la base de datos desde las variables de entorno
db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Crear motor SQLAlchemy para la conexión a la base de datos
engine = create_engine(db_url)

# Crear una sesión de SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Declarar la base para el modelo de la tabla valoracion_monedas
Base = declarative_base()

# Definir el modelo de la tabla valoracion_monedas
class ValoracionMonedas(Base):
    __tablename__ = 'valoracion_monedas'

    fecha = Column(TIMESTAMP, primary_key=True, default=datetime.now)
    moneda = Column(String)
    casa = Column(String)
    nombre = Column(String)
    compra = Column(Float)
    venta = Column(Float)
    fecha_actualizacion = Column(TIMESTAMP)

# Crear la tabla si no existe
Base.metadata.create_all(engine)

# Definir la función que ejecutará el script
def load_dollar_data():

    # Obtener los datos de la API de Dolarapi
    response = requests.get("https://dolarapi.com/v1/dolares")
    data = response.json()

    # Insertar los datos en la tabla valoracion_monedas
    for entry in data:
        moneda = ValoracionMonedas(
            moneda=entry["moneda"],
            casa=entry["casa"],
            nombre=entry["nombre"],
            compra=entry["compra"],
            venta=entry["venta"],
            fecha_actualizacion=entry["fechaActualizacion"]
        )
        session.add(moneda)
    session.commit()
    print("Datos de Dolar insertados correctamente en la tabla de valoracion_monedas.")

    # Verificar si el valor del dólar supera los 1000 y enviar una alerta por correo electrónico si es así
    if float(data[0]["venta"]) > 1000:
        enviar_alerta(float(data[0]["venta"]))

 # Obtener los datos de la API para la cotización del Euro
    response = requests.get("https://dolarapi.com/v1/cotizaciones/eur")

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # Convertir la respuesta en un diccionario
        data = response.json()

        # Insertar los datos del Euro en la tabla valoracion_monedas
        euro = ValoracionMonedas(
            moneda=data["moneda"],
            casa=data["casa"],
            nombre=data["nombre"],
            compra=data["compra"],
            venta=data["venta"],
            fecha_actualizacion=data["fechaActualizacion"]
        )
        session.add(euro)
        session.commit()
        print("Datos del Euro insertados correctamente en la tabla de valoracion_monedas.")
    else:
        print("Error al obtener los datos del Euro:", response.status_code)

    # Obtener los datos de la API para la cotización del Peso Chileno
    response = requests.get("https://dolarapi.com/v1/cotizaciones/clp")

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # Convertir la respuesta en un diccionario
        data = response.json()

        # Insertar los datos del Peso Chileno en la tabla valoracion_monedas
        peso_chileno = ValoracionMonedas(
            moneda=data["moneda"],
            casa=data["casa"],
            nombre=data["nombre"],
            compra=data["compra"],
            venta=data["venta"],
            fecha_actualizacion=data["fechaActualizacion"]
        )
        session.add(peso_chileno)
        session.commit()
        print("Datos del Peso Chileno insertados correctamente en la tabla de valoracion_monedas.")
    else:
        print("Error al obtener los datos del Peso Chileno:", response.status_code)

# Función para enviar una alerta por correo electrónico
def enviar_alerta(valor_dolar):
    mensaje = f'¡Alerta! El valor del dólar oficial es {valor_dolar}, ha superado los 1000.'
    enviar_correo(mensaje)
    
# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales del correo emisor desde las variables de entorno
correo_emisor = os.getenv('CORREO_EMISOR')
password = os.getenv('CONTRASENA_EMISOR')

def enviar_correo(mensaje):
    # Configurar el servidor SMTP
    servidor_smtp = 'smtp.especifico.com' #definir servidor de smtp
    puerto_smtp = 587

    # Configurar el mensaje de correo
    correo_destino = 'correo@destinatario.com' #definir correo del destinatario
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

if __name__ == "__main__":
    load_dollar_data()

