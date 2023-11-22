# Usa una imagen de Python como base
FROM python:3.11.6

# Establece el directorio de trabajo en el contenedor
WORKDIR /bitennial-authentication

# Copia el archivo de requisitos y luego instala las dependencias
COPY requirements.txt /bitennial-authentication/
RUN pip install -r requirements.txt

# Copia todo el código al contenedor
COPY . /bitennial-authentication/

# Expone el puerto en el que se ejecuta la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]