"""
profesor Module
"""
from flask_restful import Resource

from aplicacion.helpers.sesion import Sesion
from aplicacion.middleware.authentication import authentication
from aplicacion.modelos.profesor import ProfesorModel
from aplicacion.redis import redis_client


class Profesor(Resource):
    """
    Recurso profesor
    """
    @authentication(redis_client, Sesion())
    def get(self, rut):
        """
        Obtener profesor
        """
        profesor = ProfesorModel.buscar_por_rut(rut)
        if profesor:
            return profesor.obtener_datos()
        return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

    @authentication(redis_client, Sesion())
    def delete(self, rut):
        """
        Eliminar profesor
        """
        profesor = ProfesorModel.buscar_por_rut(rut)
        if not profesor:
            return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

        try:
            profesor.eliminar()
            return {'message': 'profesor eliminado con éxito'}
        except Exception:
            return ({'message': 'No se pudo realizar la eliminación'}, 500)
