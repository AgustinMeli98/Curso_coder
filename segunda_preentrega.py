import os
from dotenv import load_dotenv
import requests
import psycopg2
import pandas as pd

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

# Creo la tabla de estaciones_Malaga si no existe
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estaciones_Malaga (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT,
            latitud FLOAT,
            longitud FLOAT,
            direccion TEXT,
            codigo_postal INTEGER,
            poblacion TEXT,
            fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("Tabla de estaciones_Malaga creada correctamente.")

# Defino la URL de la API
url = "https://data.renfe.com/api/3/action/datastore_search?resource_id=a2368cff-1562-4dde-8466-9635ea3a572a"

# Realizo la solicitud a la API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()['result']['records']

    # Crear DataFrame a partir de los registros
    df = pd.DataFrame(data)
    
    # Descartar las columnas "Túneles lavado", "Fichas" y "Provincia", por traer datos nulos o inservibles
    df = df.drop(columns=["Túneles lavado", "Fichas", "PROVINCIA"])

    # Inserto los datos en la tabla de estaciones_Malaga
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO estaciones_Malaga (
                    codigo, descripcion, latitud, longitud,
                    direccion, codigo_postal, poblacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['CÓDIGO'],
                row['DESCRIPCION'],
                row['LATITUD'],
                row['LONGITUD'],
                row['DIRECCIÓN'],
                row['C.P.'],
                row['POBLACION']
            ))

    conn.commit()
    print("Datos insertados correctamente en la tabla de estaciones_Malaga.")
else:
    print("Error al hacer la solicitud:", response.status_code)

# Cierro la conexión
conn.close()
