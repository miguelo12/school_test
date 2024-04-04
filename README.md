# school_test
flask | docker | redis | mysql

# Init
## Alembic
- python3 -m venv aplicacion/.env
- source aplicacion/.env/bin/activate
- pip install wheel
- pip install -r aplicacion/requirements.txt
- alembic upgrade head

## Server/docker
- docker-compose up

Add secrets.py into 'aplicacion' folder

Localhost:5000 by default


Los cambios que se hicieron:

- Se agrego swagger. localhost:5000/apidocs
- Se utiliza reddis para el jwt y el cache de las apis.
- Se corrigio los errores para iniciar el proyecto.
- Se limpio el codigo para python 3.9 (hay problemas de compatibilidad con pylint, asi que no se utilizo al 100%).
- Se agrego el recurso Usuario.
- Se agrego un middleware para la autentifiacion. (Es necesario iniciar session para utilizar las apis, excepto el recurso auth)
- Se agrego paquete de python llamado alembic para migrar los cambios
que se hagan con SQLAlchemy
- Se actualiza los paquetes antiguos.
- Se eliminaron paquetes que no tenian uso o que estaban desactualizados.
- Se cambia el modelo agregando variables nuevas y index para optimizar los llamados.