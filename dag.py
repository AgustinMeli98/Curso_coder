from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import requests

# Defino la función que ejecutará el script
def load_dollar_data():

    # Cargo variables de entorno desde el archivo .env
    load_dotenv()

    # Obtengo las credenciales de la base de datos desde las variables de entorno
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    # Conecto a la base de datos de Redshift
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

    # Creo la tabla de valoracion_monedas si no existe
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS valoracion_monedas (
                fecha TIMESTAMP,
                moneda VARCHAR,
                casa VARCHAR,
                nombre VARCHAR,
                compra FLOAT,
                venta FLOAT
            )
        """)
        conn.commit()
        print("Tabla de valoracion_monedas creada correctamente.")

    # Obtengo los datos de la API de Dolarapi
    response = requests.get("https://dolarapi.com/v1/dolares")
    data = response.json()

    # Inserto los datos en la tabla de valoracion_monedas
    with conn.cursor() as cur:
        for entry in data:
            cur.execute("""
                INSERT INTO valoracion_monedas ("fecha", "moneda", "casa", "nombre", "compra", "venta")
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                datetime.now(), entry["moneda"], entry["casa"], entry["nombre"],
                entry["compra"], entry["venta"]
            ))
        conn.commit()
        print("Datos de dolar insertados correctamente en la tabla de valoracion_monedas.")
 # Obtengo los datos de la API para la cotización del Euro
    response = requests.get("https://dolarapi.com/v1/cotizaciones/eur")

    # Verifica el estado de la respuesta
    if response.status_code == 200:
        # Convierte la respuesta en un diccionario
        data = response.json()

        # Inserto los datos del Euro en la tabla de valoracion_monedas
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO valoracion_monedas ("fecha", "moneda", "casa", "nombre", "compra", "venta")
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                datetime.now(), data["moneda"], data["casa"], data["nombre"],
                data["compra"], data["venta"]
            ))
            conn.commit()
            print("Datos del Euro insertados correctamente en la tabla de valoracion_monedas.")
    else:
        print("Error al obtener los datos del Euro:", response.status_code)

    # Obtengo los datos de la API para la cotización del Peso Chileno
    response = requests.get("https://dolarapi.com/v1/cotizaciones/clp")

    # Verifica el estado de la respuesta
    if response.status_code == 200:
        # Convierte la respuesta en un diccionario
        data = response.json()

        # Inserto los datos del Peso Chileno en la tabla de valoracion_monedas
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO valoracion_monedas ("fecha", "moneda", "casa", "nombre", "compra", "venta")
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                datetime.now(), data["moneda"], data["casa"], data["nombre"],
                data["compra"], data["venta"]
            ))
            conn.commit()
            print("Datos del Peso Chileno insertados correctamente en la tabla de valoracion_monedas.")
    else:
        print("Error al obtener los datos del Peso Chileno:", response.status_code)

    # Cierro la conexión
    conn.close()


# Llamo a la función para cargar los datos de Dolar
load_dollar_data()

