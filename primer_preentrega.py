#importar API y crear tabla con columnas correspondientes en Redshift, con columna temporal de control

import requests
import psycopg2

# Conecto a la base de datos de Redshift
conn = psycopg2.connect(
    host='data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
    port='5439',
    dbname='data-engineer-database',
    user='agusmeli98_coderhouse',
    password='S8osw1x5Bl'
)

# Defino la URL de la API
url = "https://api.covidtracking.com/v1/states/current.json"

# Realizo la solicitud a la API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Obtengo las claves (columnas) de un registro de datos para crear la tabla
    sample_record = data[0]  # Tomo el primer registro como muestra
    columns = list(sample_record.keys())

    # Creo la tabla en Redshift
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS covid_data")  # Elimino la tabla si ya existe
        cur.execute("CREATE TABLE covid_data ({})".format(', '.join([f"{column} VARCHAR" for column in columns])))
        # Agrego columna para la fecha de ingesta
        cur.execute("ALTER TABLE covid_data ADD COLUMN fecha_ingesta DATE DEFAULT CURRENT_DATE")
    conn.commit()

    print("Tabla creada correctamente.")
else:
    print("Error al hacer la solicitud:", response.status_code)

# Cierro la conexión
conn.close()
