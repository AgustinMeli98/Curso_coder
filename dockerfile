# Utilizo una imagen de Python como base
FROM python:3.8-slim

# Instalo Airflow y otras dependencias
RUN pip install apache-airflow[yaml,postgres]
RUN pip install yfinance 

# Establezco las variables de entorno para Airflow
ENV AIRFLOW_HOME=/airflow
ENV PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"

# Creo el directorio para los DAGs
RUN mkdir -p /airflow/dags

# Copio el script de DAG al directorio de DAGs en el contenedor
COPY dag.py /airflow/dags/

# Inicio Airflow al iniciar el contenedor
CMD ["airflow", "webserver", "--port", "8080"]
