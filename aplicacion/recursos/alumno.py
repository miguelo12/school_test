"""
Alumno Module
"""
from flask_restful import Resource

from aplicacion.modelos.alumno import AlumnoModel


class Alumno(Resource):
    """
    Recursos alumno
    """

    def get(self, rut):
        """
        Obtener alumno
        """
        alumno = AlumnoModel.buscar_por_rut(rut)

        if alumno:
            return alumno.obtener_datos()

        return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

    def delete(self, rut):
        """
        Eliminar alumno
        """
        alumno = AlumnoModel.buscar_por_rut(rut)

        if not alumno:
            return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

        try:
            alumno.eliminar()
            return {'message': 'Alumno eliminado con éxito'}
        except Exception:
            return ({'message': 'No se pudo realizar la eliminación'}, 500)
