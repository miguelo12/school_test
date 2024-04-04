"""
alumnos curso Module
"""
from flask_restful import Resource
from flask_restful import reqparse

from aplicacion.helpers.sesion import Sesion
from aplicacion.middleware.authentication import authentication
from aplicacion.modelos.alumno import AlumnoModel
from aplicacion.modelos.curso import CursoModel
from aplicacion.redis import redis_client


class AlumnosCurso(Resource):
    """
    Recurso alumnos curso
    """
    parser_post = reqparse.RequestParser()
    parser_post.add_argument(
        'rut_alumno',
        type=str,
        required=True,
        help='Debe ingresar el alumno que va ingresar al curso'
    )

    @authentication(redis_client, Sesion())
    def get(self, nombre):
        """
        Obtiene los alumnos de un curso
        ---
        tags:
          - alumnos_curso
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
          - name: nombre
            in: path
            type: string
            required: true
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {
                    }
        """
        curso = CursoModel.buscar_por_nombre(nombre)
        if curso:
            return curso.obtener_alumnos()
        return ({'mensaje': 'No se encontró el curso solicitado'}, 404)

    @authentication(redis_client, Sesion())
    def post(self, nombre):
        """
        Obtiene los alumnos de un curso
        ---
        tags:
          - alumnos_curso
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
          - name: nombre
            in: path
            type: string
            required: true
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {"message": "Guardado con exito"}
        """
        data = self.parser_post.parse_args()
        rut_alumno = data['rut_alumno']

        alumno = AlumnoModel.buscar_por_rut(rut_alumno)
        curso = CursoModel.buscar_por_nombre(nombre)

        if not curso:
            return ({'mensaje': 'No se encontró el curso'}, 404)
        if not alumno:
            return ({'mensaje': 'No se encontró el alumno'}, 404)

        try:
            curso.alumnos.append(alumno)
            curso.guardar()
            return ({'mensaje': 'Guardado con exito'}, 200)
        except Exception as e:
            return ({'message': f'No se pudo resolver su petición. {e}'}, 500)
