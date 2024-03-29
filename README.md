# Proyecto de curso de data engineering

## Objetivo primer entregable

El primer entregable del proyecto consta de formular una consulta sobre una API, y crear una tabla en redshift para albergar y consumir los datos consultados. 
En nuestro caso trabajamos con datos de transporte público (trenes) en España. URL: 	https://data.renfe.com/api/3/action/datastore_search

## Objetivo segundo entregable
Solucionar una situación real de ETL donde puedan llegar a aparecer duplicados, nulos y valores atípicos durante la ingesta- Transformación- Carga de la data

## Pasos para utilización:

**1_ Copiar repositorio.**

**2_ Instalar las dependencias con comando:** `pip install -r requirements.txt`.

**3_ Ejecutar el script principal con el comando:** `python Primer_entregable.py`.

### En cuanto a los requerimientos: 
* psycopg2: Es necesario para conectarse y operar con la base de datos PostgreSQL. Este módulo proporciona una implementación de la API de bases de datos de PostgreSQL para Python.
* requests: Se utiliza para realizar solicitudes HTTP a la API externa y obtener los datos necesarios.
* python-dotenv: Esta biblioteca facilita la carga de variables de entorno desde archivos .env en tu sistema.
