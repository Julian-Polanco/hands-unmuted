FROM python:3.11-slim

# Establecer variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app/api

# Instalar dependencias del sistema si son necesarias


# Copiar el archivo de requerimientos e instalar las dependencias de Python
COPY src/web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Copiar el directorio del modelo
COPY models /app/api/models

# Copiar el código de la aplicación Django
COPY src/web/api /app/api

RUN python manage.py collectstatic --noinput

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación usando Gunicorn
# Asegúrate de que 'api.wsgi' coincide con la estructura de tu proyecto
CMD ["gunicorn", "api.wsgi:application", "--bind", "0.0.0.0:8000"]