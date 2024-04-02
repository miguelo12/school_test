"""
alumnos curso Module
"""
from flask_restful import Resource

from aplicacion.modelos.curso import CursoModel


class AlumnosCurso(Resource):
    """
    Recurso alumnos curso
    """
    def get(self, nombre):
        """
        Obtiene los alumnos de un curso
        """
        curso = CursoModel.buscar_por_nombre(nombre)
        if curso:
            return curso.obtener_alumnos()
        return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)
