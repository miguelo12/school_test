"""
usuario Module
"""
from flask_restful import Resource

from aplicacion.helpers.sesion import Sesion
from aplicacion.middleware.authentication import authentication
from aplicacion.modelos.usuario import UsuarioModel
from aplicacion.redis import redis_client


class Usuario(Resource):
    """
    Recurso Usuario
    """

    @authentication(redis_client, Sesion())
    def get(self, _id):
        """
        Obtener el usuario mediante el id
        ---
        tags:
          - user
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'usuario': {}}
        """
        usuario = UsuarioModel.buscar_por_id(_id)
        if usuario:
            return usuario.obtener_datos()
        return ({'mensaje': 'No se encontró el usuario'}, 404)
