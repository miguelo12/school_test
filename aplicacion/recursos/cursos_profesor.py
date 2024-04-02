"""
profesores Module
"""
from flask_restful import Resource

from aplicacion.helpers.sesion import Sesion
from aplicacion.middleware.authentication import authentication
from aplicacion.modelos.profesor import ProfesorModel
from aplicacion.redis import redis_client


class CursosProfesor(Resource):
    """
    Recurso curso profesor
    """
    @authentication(redis_client, Sesion())
    def get(self, rut):
        """
        obtener los cursos del profesor
        """
        profesor = ProfesorModel.buscar_por_rut(rut)

        if not profesor:
            return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

        cursos = profesor.cursos
        lista_cursos = {}

        for curso in cursos:
            lista_cursos[curso.id] = {
                "nombre": curso.nombre,
                "nivel": curso.nivel
            }

        data_profesor = profesor.obtener_datos()
        data_profesor['cursos'] = lista_cursos
        return data_profesor
