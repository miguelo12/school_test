"""
usuarios Module
"""
from flask_restful import Resource
from flask_restful import reqparse

from aplicacion.helpers.sesion import Sesion
from aplicacion.middleware.authentication import authentication
from aplicacion.modelos.usuario import UsuarioModel
from aplicacion.redis import redis_client


class Usuarios(Resource):
    """
    Recurso usuarios
    """
    # Post
    parser_post = reqparse.RequestParser()
    parser_post.add_argument(
        'username',
        type=str,
        required=True,
        help='Debe ingresar un usuario'
    )
    parser_post.add_argument(
        'password',
        type=str,
        required=True,
        help='Debe ingresar una password'
    )

    # Update
    parser_put = reqparse.RequestParser()
    parser_put.add_argument(
        'username',
        type=str,
        required=True,
        help='Debe ingresar un usuario'
    )
    parser_put.add_argument(
        'password',
        type=str,
        required=True,
        help='Debe ingresar una password'
    )
    parser_put.add_argument(
        'activo',
        type=bool,
        required=False
    )

    # Delete
    parser_delete = reqparse.RequestParser()
    parser_delete.add_argument(
        'username',
        type=str,
        required=True,
        help='Debe ingresar un usuario'
    )

    @authentication(redis_client, Sesion())
    def get(self):
        """
        Obtener los usuarios
        ---
        tags:
          - users
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'usuarios': []}
        """
        return {'usuarios': list(map(lambda x: x.obtener_datos(), UsuarioModel.query.all()))}

    def post(self):
        """
        Crear un nuevo usuario
        ---
        tags:
          - users
        parameters:
          - name: user
            in: body
            schema:
                type: object
                required:
                - username
                - password
                properties:
                    username:
                        type: string
                        maxLength: 100
                    password:
                        type: string
                        maxLength: 100
                    activo:
                        type: boolean
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'message': 'Usuario guardado con éxito'}
        """
        data = self.parser_post.parse_args()
        username = str(data['username'])
        password = str(data['password'])

        if UsuarioModel.buscar_username(username):
            return ({'message': 'Ya existe el usuario'}, 400)

        salt, hash_pass = Sesion().generate_hash(password)
        user_model = UsuarioModel(username, hash_pass, salt)

        try:
            user_model.guardar()
            return {'message': 'Alumno guardado con éxito'}
        except Exception:
            return ({'message': 'No se pudo guardar el usuario'}, 400)

    @authentication(redis_client, Sesion())
    def put(self):
        """
        Actualizar usuario
        ---
        tags:
          - users
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
          - name: user
            in: body
            schema:
                type: object
                required:
                - username
                - password
                properties:
                    username:
                        type: string
                        maxLength: 100
                    password:
                        type: string
                        maxLength: 100
                    activo:
                        type: boolean
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'message': 'Usuario guardado con éxito'}
        """
        data = self.parser_put.parse_args()
        sesion = Sesion()
        username = data['username']
        password = data['password']
        activo = data['activo']
        is_change = False

        user_model = UsuarioModel.buscar_username(username)
        if not user_model:
            return ({'message': 'No existe el usuario'}, 400)

        # Si son distintos se cambia el password
        __, hash_pass_form = sesion.generate_hash(password, salt=user_model.salt)
        if user_model.password != hash_pass_form:
            salt, hash_pass = sesion.generate_hash(password)
            user_model.password = hash_pass
            user_model.salt = salt
            is_change = True

        # Actualiza si esta activo o no el usuario
        if activo is not None and activo != user_model.activo:
            user_model.activo = activo
            is_change = True

        # Si no existen cambios lo reenvia, previene guardar a la base de datos.
        if not is_change:
            return ({'message': 'No hubo cambios'}, 202)

        try:
            user_model.guardar()
            return {'message': 'Usuario guardado con éxito'}
        except Exception:
            return ({'message': 'No se pudo guardar el usuario'}, 400)

    @authentication(redis_client, Sesion())
    def delete(self):
        """
        Eliminar usuario
        ---
        tags:
          - users
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
          - name: alumnos
            in: body
            schema:
                type: object
                required:
                - username
                properties:
                    username:
                        type: string
                        maxLength: 100
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'message': 'Usuario eliminado con éxito'}
        """
        data = self.parser_delete.parse_args()
        username = str(data['username'])

        usuario_model = UsuarioModel.buscar_username(username)

        if not usuario_model:
            return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

        try:
            usuario_model.eliminar()
            return {'message': 'Usuario eliminado con éxito'}
        except Exception:
            return ({'message': 'No se pudo eliminar el usuario'}, 400)
