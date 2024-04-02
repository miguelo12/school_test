"""
cursos_alumno Module
"""
from flask_restful import Resource

from aplicacion.modelos.alumno import AlumnoModel


class CursosAlumno(Resource):
    """
    Recurso cursos alumno
    """

    def get(self, rut):
        """
        Obtiene los cursos del alumno
        """
        alumno = AlumnoModel.buscar_por_rut(rut)

        if not alumno:
            return ({'mensaje': 'No se encontró el recurso solicitado'}, 404)

        cursos = alumno.cursos
        lista_cursos = {}
        for curso in cursos:
            data_profesor = {
                'id': curso.profesor_id,
                'nombres': curso.profesor.nombres,
                'apellidos': curso.profesor.apellidos
            }
            lista_cursos[curso.id] = {
                "nombre": curso.nombre,
                "nivel": curso.nivel,
                "profesor_id": curso.profesor_id,
                "profesor": data_profesor
            }

        data_alumno = alumno.obtener_datos()
        data_alumno['cursos'] = lista_cursos
        return data_alumno
