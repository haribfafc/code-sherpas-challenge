# Usa una imagen base oficial de Python 3
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos de la aplicación al contenedor
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto en el directorio de trabajo
COPY . .

# Exponer el puerto en el que correrá Django (normalmente 8000)
EXPOSE 8000

# Configurar las variables de entorno de Django
ENV DJANGO_SETTINGS_MODULE=project.settings
ENV PYTHONUNBUFFERED=1

# Recuerda cambiar 'myproject' por el nombre de tu proyecto en 'myproject.settings'
# Se asegura que todas las migraciones estén aplicadas al iniciar el contenedor
RUN python manage.py migrate

# Define el comando de ejecución que corre el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
