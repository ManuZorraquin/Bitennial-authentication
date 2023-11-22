# Bitennial-authentication
## Resumen
Este proyecto está basado en Web APIs de autenticación de usuarios. Incluye acciones como registro, inicio de sesión, visualización y edición de datos del usuario. También se implementaron medidas de autenticación de usuario mediante JWT (JSON Web Tokens).

## Instalación

Ejecuta los siguientes comandos de docker-compose para instalar las dependencias del proyecto y levantar el contenedor de Docker:

```bash
docker-compose build
docker-compose up
```

## Prueba de Endpoints en Postman
Puedes probar los endpoints utilizando Postman. Para esto, entrá a este link, copiá el contenido e importalo en Postman. URL:  https://api.postman.com/collections/26913797-c69102e2-8415-4e39-8417-1fe67dc9cb0f?access_key=PMAT-01HFW00FVX4NRMFWJ9AV6H8A9C


## Ejecución de pruebas por consola
Entra al contenedor Docker: Con el contenedor levantado (docker-compose up), ejecuta el siguiente comando en la consola:
```bash
docker-compose exec web bash
```
Luego dentro del contenedor: 
```bash
python manage.py test authentication_app.tests.test_views
```
