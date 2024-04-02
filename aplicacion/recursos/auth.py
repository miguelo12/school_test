"""
auth Module
"""
from datetime import timedelta

from flask import current_app
from flask_restful import Resource
from flask_restful import reqparse

from aplicacion.helpers.sesion import Sesion
from aplicacion.modelos.usuario import UsuarioModel
from aplicacion.redis import redis_client as redis


class Auth(Resource):
    """
    Recurso de autenticación
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Debe ingresar un usuario'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Debe ingresar una password'
    )

    parser_delete = reqparse.RequestParser()
    parser_delete.add_argument('Authorization', location='headers')

    def post(self):
        """
        Iniciar sesion
        ---
        tags:
          - auth
        parameters:
          - name: username
            in: body
            type: string
            required: true
          - name: password
            in: body
            type: string
            required: true
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'message': 'Se cerro la sesion'}
        """
        session = Sesion()
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        redis_invalid = redis.get(f'{username}-invalid')
        invalid = int(str(redis_invalid)) if redis_invalid else 0

        if invalid >= 3:
            return ({'message': 'Usuario bloqueado temporalmente'}, 400)

        jwt_secret_key = current_app.config['JWT_SECRET_KEY']
        jwt_lifetime_hours = current_app.config['JWT_LIFETIME_HOURS']

        usuario_model = UsuarioModel.buscar_username(username)

        if not usuario_model:
            return ({'message': 'No existe el usuario'}, 400)

        # Verifica que la contraseña sea la misma
        __, pass_session = session.generate_hash(password, usuario_model.salt)
        if pass_session == usuario_model.password:
            token = session.generar_token(
                redis,
                jwt_secret_key,
                timedelta(minutes=jwt_lifetime_hours),
                usuario_model.id,
                {
                    'usuario': usuario_model.username
                }
            )
            return {'message': 'Inicio de session exitosa.', 'data': {'token': token}}

        # Fallo la password
        invalid += 1
        redis.set(f'{username}-invalid', invalid, ex=timedelta(seconds=15))
        return ({'mensaje': 'Contraseña invalida'}, 404)

    def delete(self):
        """
        Cerrar sesion
        ---
        tags:
          - auth
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'message': 'Se cerro la sesion'}
        """
        sesion = Sesion()
        data = self.parser_delete.parse_args()
        jwt_token = data['Authorization']

        jwt_secret_key = current_app.config['JWT_SECRET_KEY']
        decode_jwt = sesion.decode_jwt(jwt_token, jwt_secret_key)
        username = decode_jwt.get('usuario')

        user_model = UsuarioModel.buscar_username(username)
        if not user_model:
            return ({'mensaje': 'No existe este usuario, para cerrar la sesion'}, 404)

        if sesion.eliminar_token(redis, jwt_token):
            return {'message': 'Se cerro la sesion'}

        return ({'message': 'No se pudo cerrar sesion'}, 500)
