# Utilizo una imagen de Python como base
FROM python:3.8-slim

# Copio el archivo de requisitos y lo instalo
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copio los scripts al contenedor
COPY cargar_datos.py /app/cargar_datos.py
COPY enviar_alerta.py /app/enviar_alerta.py

# Establezco el directorio de trabajo
WORKDIR /app

# Ejecuto el script de cargar_datos
CMD ["python", "cargar_datos.py"]
