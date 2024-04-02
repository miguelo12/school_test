"""
curso Module
"""
from flask_restful import Resource
from flask_restful import reqparse

from aplicacion.helpers.sesion import Sesion
from aplicacion.middleware.authentication import authentication
from aplicacion.modelos.curso import CursoModel
from aplicacion.modelos.profesor import ProfesorModel
from aplicacion.redis import redis_client


class Cursos(Resource):
    """
    Recurso cursos
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'nombre',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el curso"
    )
    parser.add_argument(
        'rut_profesor',
        type=str,
        required=True,
        help="Debe ingresar el rut del profesor que dictará el curso."
    )
    parser.add_argument(
        'nivel',
        type=int,
        required=True,
        choices=(1, 2, 3, 4),
        help="Debe ingresar el nivel (entero del 1 al 4)."
    )
    parser.add_argument(
        'activo',
        type=bool,
        required=False
    )

    @authentication(redis_client, Sesion())
    def get(self):
        """
        Obtener cursos
        """
        return {'cursos': list(map(lambda x: x.obtener_datos(), CursoModel.query.all()))}

    @authentication(redis_client, Sesion())
    def post(self):
        """
        Guardar curso
        """
        data = Cursos.parser.parse_args()
        rut_profesor = data['rut_profesor']
        nombre = data['nombre']
        nivel = data['nivel']
        activo = data['activo']

        if CursoModel.buscar_existencia(nombre):
            return (
                {'message': f'Ya existe un curso llamado \'{nombre}\'.'},
                400
            )

        profesor = ProfesorModel.buscar_por_rut(rut_profesor)
        if not profesor:
            return ({'message': 'El identificador del profesor ingresado no es válido'}, 400)

        curso = CursoModel(nombre, profesor.id, nivel)

        if activo is not None:
            curso.activo = activo

        try:
            curso.guardar()
        except Exception:
            return ({'message': 'No se pudo resolver su petición.'}, 500)

        return curso.obtener_datos(), 201
