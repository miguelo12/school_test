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


class Curso(Resource):
    """
    El recurso de curso
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'nombre',
        type=str,
        required=True,
        help='Debe ingresar un nombre para el curso'
    )
    parser.add_argument(
        'rut_profesor',
        type=str,
        required=True,
        help='Debe ingresar el rut del profesor que dictará el curso.'
    )
    parser.add_argument(
        'nivel',
        type=int,
        required=True,
        choices=(1, 2, 3, 4),
        help='Debe ingresar el nivel (entero del 1 al 4).'
    )
    parser.add_argument(
        'activo',
        type=bool,
        required=False
    )

    @authentication(redis_client, Sesion())
    def get(self, nombre):
        """
        Obtener curso
        ---
        tags:
          - curso
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
                    application/json: {}
        """
        curso = CursoModel.buscar_por_nombre(nombre)
        if curso:
            return curso.obtener_datos()
        return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

    @authentication(redis_client, Sesion())
    def delete(self, nombre):
        """
        Elimina el curso
        ---
        tags:
          - curso
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
                    application/json: {"message": "Curso eliminado con éxito"}
        """
        curso = CursoModel.buscar_por_nombre(nombre)
        if not curso:
            return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

        try:
            curso.eliminar()
            return {'message': 'Curso eliminado con éxito'}
        except Exception:
            return ({'message': 'No se pudo realizar la eliminación'}, 500)

    @authentication(redis_client, Sesion())
    def put(self, nombre):
        """
        Actualizar curso
        ---
        tags:
          - curso
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
          - name: nombre
            in: path
            type: string
            required: true
          - name: curso
            in: body
            schema:
                type: object
                required:
                - nombre
                - rut_profesor
                - nivel
                - activo
                properties:
                    nombre:
                        type: string
                        maxLength: 100
                    rut_profesor:
                        type: string
                        maxLength: 15
                    nivel:
                        type: integer
                        maxLength: 1
                    activo:
                        type: boolean
        responses:
            201:
                description: Respuesta exitosa.
                examples:
                    application/json: {}
        """
        data = self.parser.parse_args()
        curso_model = CursoModel.buscar_por_nombre(nombre)

        if not curso_model:
            return ({'message': 'No se encontró el curso'}, 404)

        profesor = ProfesorModel.buscar_por_rut(data['rut_profesor'])
        if not profesor:
            return ({'message': 'El identificador del profesor ingresado no es válido'}, 400)

        curso_model.nombre = data['nombre']
        curso_model.profesor_id = profesor.id
        curso_model.nivel = data['nivel']

        activo = data['activo']
        if activo is not None:
            curso_model.activo = activo

        try:
            curso_model.guardar()
        except Exception:
            return ({'message': 'No se pudo resolver su petición.'}, 500)

        return (curso_model.obtener_datos(), 201)
