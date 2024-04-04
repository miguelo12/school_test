"""
profesores Module
"""
from flask_restful import Resource
from flask_restful import reqparse

from aplicacion.helpers.sesion import Sesion
from aplicacion.middleware.authentication import authentication
from aplicacion.modelos.profesor import ProfesorModel
from aplicacion.redis import redis_client


class Profesores(Resource):
    """
    Recurso profesores
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'nombres',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el profesor"
    )
    parser.add_argument(
        'apellidos',
        type=str,
        required=True,
        help="Debe ingresar un apellido para el profesor."
    )
    parser.add_argument(
        'rut',
        type=str,
        required=True,
        help="Debe ingresar un rut para el profesor."
    )
    parser.add_argument(
        'activo',
        type=bool,
        required=False
    )

    @authentication(redis_client, Sesion())
    def get(self):
        """
        Obtener profesores
        ---
        tags:
          - profesores
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {}
        """
        return ({'Profesores': list(map(lambda x: x.obtener_datos(), ProfesorModel.query.all()))})

    @authentication(redis_client, Sesion())
    def post(self):
        """
        Agregar profesor
        ---
        tags:
          - profesores
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
          - name: profesores
            in: body
            schema:
                type: object
                required:
                - nombres
                - apellidos
                - rut
                - activo
                properties:
                    nombres:
                        type: string
                        maxLength: 100
                    apellidos:
                        type: string
                        maxLength: 100
                    rut:
                        type: string
                        maxLength: 15
                    activo:
                        type: boolean
        responses:
            201:
                description: Respuesta exitosa.
                examples:
                    application/json: {}
        """
        data = Profesores.parser.parse_args()
        if ProfesorModel.buscar_existencia(data['rut']):
            return (
                {
                    'message': f"Ya existe un profesor llamado '{data['nombres']}"
                               f"{data['apellidos']}'. Uno es suficiente!"
                },
                400
            )

        profesor = ProfesorModel(data['nombres'], data['apellidos'], data['rut'])

        activo = data['activo']
        if activo is not None:
            profesor.activo = activo

        try:
            profesor.guardar()
        except Exception:
            return ({'message': 'No se pudo resolver su petición.'}, 500)
        return (profesor.obtener_datos(), 201)

    @authentication(redis_client, Sesion())
    def put(self):
        """
        Actualizar profesor
        ---
        tags:
          - profesores
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
          - name: profesores
            in: body
            schema:
                type: object
                required:
                - nombres
                - apellidos
                - rut
                - activo
                properties:
                    nombres:
                        type: string
                        maxLength: 100
                    apellidos:
                        type: string
                        maxLength: 100
                    rut:
                        type: string
                        maxLength: 15
                    activo:
                        type: boolean
        responses:
            201:
                description: Respuesta exitosa.
                examples:
                    application/json: {}
        """
        data = Profesores.parser.parse_args()
        profesor = ProfesorModel.buscar_existencia(data['rut'])

        if not profesor:
            return ({'message': 'No se pudo resolver su petición.'}, 400)

        profesor.nombres = data['nombres']
        profesor.apellidos = data['apellidos']

        activo = data['activo']
        if activo is not None:
            profesor.activo = activo

        try:
            profesor.guardar()
        except Exception:
            return ({'message': 'No se pudo resolver su petición.'}, 500)

        return (profesor.obtener_datos(), 201)
