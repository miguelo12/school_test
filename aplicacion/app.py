"""
App flask
"""
from flasgger import Swagger
from flask import Flask
from flask_caching import Cache
from flask_restful import Api

from aplicacion.config import app_config
from aplicacion.db import db
from aplicacion.recursos.alumno import Alumno
from aplicacion.recursos.alumnos import Alumnos
from aplicacion.recursos.alumnos_curso import AlumnosCurso
from aplicacion.recursos.auth import Auth
from aplicacion.recursos.curso import Curso
from aplicacion.recursos.cursos import Cursos
from aplicacion.recursos.cursos_alumno import CursosAlumno
from aplicacion.recursos.cursos_profesor import CursosProfesor
from aplicacion.recursos.profesor import Profesor
from aplicacion.recursos.profesores import Profesores
from aplicacion.recursos.usuario import Usuario

# IMPORTACIÓN DE RECURSOS
app = Flask(__name__)

# Se establece enviroment como argumento
ENVIROMENT = "development"  # sys.argv[1]

# Se setean variables de configuracion segun ambiente(env)
app.config.from_object(app_config[ENVIROMENT])

# Initialize Flask-Caching with Redis and DB
cache = Cache(app=app)
db.init_app(app)

# SE DEFINEN LOS ENDPOINTS Y LA CLASE QUE SE ENCARGARÁ DE PROCESAR CADA SOLICITUD
api = Api(app)
swagger = Swagger(app, template={
    "info": {
        "title": "API Colegio",
        "description": "API donde se pueden agregar alumnos y profesores en cursos",
        "version": "1.0.0"
    }
})

api.add_resource(Alumno, '/alumno/<string:rut>')
api.add_resource(Alumnos, '/alumnos')
api.add_resource(CursosAlumno, '/alumno/<string:rut>/cursos')
api.add_resource(Profesor, '/profesor/<string:rut>')
api.add_resource(CursosProfesor, '/profesor/<string:rut>/cursos')
api.add_resource(Profesores, '/profesores')
api.add_resource(Curso, '/curso/<string:nombre>')
api.add_resource(Cursos, '/cursos')
api.add_resource(AlumnosCurso, '/curso/<string:nombre>/alumnos')
api.add_resource(Auth, '/auth')
api.add_resource(Usuario, '/user')

app.run(host='0.0.0.0', port=5000)
