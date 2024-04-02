"""
profesor Module
"""
from flask_restful import Resource

from aplicacion.modelos.profesor import ProfesorModel


class Profesor(Resource):
    """
    Recurso profesor
    """

    def get(self, rut):
        """
        Obtener profesor
        """
        profesor = ProfesorModel.buscar_por_rut(rut)
        if profesor:
            return profesor.obtener_datos()
        return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

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
