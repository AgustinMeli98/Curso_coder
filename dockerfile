# Utilizo una imagen de Python como base
FROM python:3.8-slim

# Copio el archivo de requisitos y lo instalo
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copio el script al contenedor
COPY dag.py /app/dag.py

# Establezco el directorio de trabajo
WORKDIR /app

# Ejecuto el script
CMD ["python", "dag.py"]


