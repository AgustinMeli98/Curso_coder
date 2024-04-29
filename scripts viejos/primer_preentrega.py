import os
from dotenv import load_dotenv
import requests
import psycopg2

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

# Creo la tabla de estaciones si no existe
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estaciones (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT,
            latitud FLOAT,
            longitud FLOAT,
            direccion TEXT,
            codigo_postal INTEGER,
            poblacion TEXT,
            provincia TEXT,
            fichas TEXT,
            tuneles_lavado TEXT,
            fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("Tabla de estaciones creada correctamente.")

# Defino la URL de la API
url = "https://data.renfe.com/api/3/action/datastore_search?resource_id=a2368cff-1562-4dde-8466-9635ea3a572a"

# Realizo la solicitud a la API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()['result']['records']

    # Inserto los datos en la tabla de estaciones
    with conn.cursor() as cur:
        for record in data:
            cur.execute("""
                INSERT INTO estaciones (
                    codigo, descripcion, latitud, longitud,
                    direccion, codigo_postal, poblacion, provincia,
                    fichas, tuneles_lavado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record['CÓDIGO'],
                record['DESCRIPCION'],
                record['LATITUD'],
                record['LONGITUD'],
                record['DIRECCIÓN'],
                record['C.P.'],
                record['POBLACION'],
                record['PROVINCIA'],
                record['Fichas'],
                record['Túneles lavado']
            ))

    conn.commit()
    print("Datos insertados correctamente en la tabla de estaciones.")
else:
    print("Error al hacer la solicitud:", response.status_code)

# Cierro la conexión
conn.close()
