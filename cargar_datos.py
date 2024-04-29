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

if __name__ == "__main__":
    load_dollar_data()
