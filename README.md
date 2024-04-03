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
