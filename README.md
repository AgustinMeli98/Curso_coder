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

## CAMBIO DE API  
En función de obtener datos reelevantes y actualizables diariamente, decidí cambiar la API utilizada en el tercer entregable por la de yahoo finance de bitcoin, en la cual obtengo datos sobre los valores diarios del bitcoin.

## Objetivo tercer entregable
* Crear un script liviano y funcional que pueda ser utilizado en cualquier Sistema operativo y por cualquier usuario. 

* Dockerizar un script para hacerlo funcional en cualquier sistema operativo. 


## Proyecto final
Se cambió la API utilizada para obtener valores más confiables y de actualización más continua.

### Construcción de imagen de docker
docker build -t carga_datos_moneda .

### Crear y ejecutar contenedor:
docker run --name contenedor_moneda carga_datos_moneda

