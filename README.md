# school_test
flask | docker | redis | mysql

docker
======

# Init

# Alembic
- python3 -m venv aplicacion/.env
- source aplicacion/.env/bin/activate
- pip install -r aplicacion/requirements.txt
- alembic upgrade head

# Servers
- docker-compose up
o
- docker-compose up --build

Add secrets.py into 'aplicacion' folder
Localhost:5000 by default
