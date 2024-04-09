from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import yfinance as yf


# Defino la función que ejecutará el script
def load_bitcoin():

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

    # Creo la tabla de Bitcoin si no existe
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin (
                datetime TIMESTAMP,
                "open" FLOAT,
                "high" FLOAT,
                "low" FLOAT,
                "close" FLOAT,
                "adj_close" FLOAT,
                "volume" BIGINT
            )
        """)
        conn.commit()
        print("Tabla de Bitcoin creada correctamente.")

    # Leo los datos de finanzas de Bitcoin desde un DataFrame de pandas
    # Símbolo de Bitcoin en Yahoo Finance
    bitcoin_symbol = "BTC-USD"

    # Obtengo datos de Bitcoin por hora
    df = yf.download(bitcoin_symbol, period="1d", interval="1h")

    # Inserto los datos en la tabla de Bitcoin
    with conn.cursor() as cur:
        for datetime, row in df.iterrows():
            cur.execute("""
                INSERT INTO bitcoin ("datetime", "open", "high", "low", "close", "adj_close", "volume")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                datetime, row["Open"], row["High"], row["Low"], row["Close"], row["Adj Close"], row["Volume"]
            ))
        conn.commit()
        print("Datos insertados correctamente en la tabla de Bitcoin.")

    # Cierro la conexión
    conn.close()


# Llamo a la función para cargar los datos de Bitcoin
load_bitcoin()
