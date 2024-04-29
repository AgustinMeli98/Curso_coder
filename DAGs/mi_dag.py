from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

# Importar las funciones de los scripts
from cargar_datos import load_dollar_data
from enviar_alerta import enviar_correo

# Cargar variables de entorno desde el archivo .env
from dotenv import load_dotenv
load_dotenv()

# Obtener las credenciales del correo emisor desde las variables de entorno
correo_emisor = os.getenv('CORREO_EMISOR')

# Definir los argumentos del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir la función para verificar y enviar la alerta
def verificar_y_enviar_alerta(**kwargs):
    # Obtener el valor del dólar
    valor_dolar = kwargs['task_instance'].xcom_pull(task_ids='cargar_datos')['venta']

    # Verificar si el valor del dólar supera los 1000 y enviar una alerta por correo electrónico si es así
    if valor_dolar > 1000:
        mensaje = f'¡Alerta! El valor del dólar oficial es {valor_dolar}, ha superado los 1000.'
        enviar_correo(mensaje)

# Definir la programación del DAG
with DAG('cargar_datos_y_enviar_alerta',
         default_args=default_args,
         description='Cargar datos y enviar alerta si el valor del dólar supera 1000',
         schedule_interval='@daily',
         start_date=datetime(2024, 1, 1),
         catchup=False) as dag:

    # Tarea para cargar los datos
    cargar_datos = PythonOperator(
        task_id='cargar_datos',
        python_callable=load_dollar_data,
        provide_context=True
    )

    # Tarea para verificar y enviar la alerta
    enviar_alerta = PythonOperator(
        task_id='enviar_alerta',
        python_callable=verificar_y_enviar_alerta,
        provide_context=True
    )

    # Definir la secuencia de tareas
    cargar_datos >> enviar_alerta
