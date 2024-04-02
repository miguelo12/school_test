"""
authentication module
"""
from functools import wraps
from typing import TYPE_CHECKING

from flask import request

if TYPE_CHECKING:
    from flask_restful import Resource
    from redis import Redis

    from aplicacion.helpers.sesion import Sesion


def authentication(redis: 'Redis', sesion: 'Sesion'):
    """
    Revisar si el usuario esta logueado.
    """
    def _authentication(f):
        @wraps(f)
        def __authentication(*args, **kwargs):
            authorization = request.headers.get('Authorization')

            if not authorization:
                return ({'message': 'Necesitas un token de acceso'}, 400)

            if not sesion.validar_token(redis, authorization):
                return ({'message': 'No es valido el token'}, 400)

            result = f(*args, **kwargs)
            return result
        return __authentication
    return _authentication
