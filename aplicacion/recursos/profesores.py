"""
profesores Module
"""
from flask_restful import Resource
from flask_restful import reqparse

from aplicacion.modelos.profesor import ProfesorModel


class Profesores(Resource):
    """
    Recurso profesores
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'nombres',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el profesor"
    )
    parser.add_argument(
        'apellidos',
        type=str,
        required=True,
        help="Debe ingresar un apellido para el profesor."
    )
    parser.add_argument(
        'rut',
        type=str,
        required=True,
        help="Debe ingresar un rut para el profesor."
    )
    parser.add_argument(
        'activo',
        type=bool,
        required=False
    )

    def get(self):
        """
        Obtener profesores
        """
        return ({'Profesores': list(map(lambda x: x.obtener_datos(), ProfesorModel.query.all()))})

    def post(self):
        """
        Agregar profesor
        """
        data = Profesores.parser.parse_args()
        if ProfesorModel.buscar_existencia(data['rut']):
            return (
                {
                    'message': f"Ya existe un profesor llamado '{data['nombres']}"
                               f"{data['apellidos']}'. Uno es suficiente!"
                },
                400
            )

        profesor = ProfesorModel(data['nombres'], data['apellidos'], data['rut'])

        activo = data['activo']
        if activo is not None:
            profesor.activo = activo

        try:
            profesor.guardar()
        except Exception:
            return ({'message': 'No se pudo resolver su petición.'}, 500)
        return (profesor.obtener_datos(), 201)

    def put(self):
        """
        Actualizar profesor
        """
        data = Profesores.parser.parse_args()
        profesor = ProfesorModel.buscar_existencia(data['rut'])

        if not profesor:
            return ({'message': 'No se pudo resolver su petición.'}, 400)

        profesor.nombres = data['nombres']
        profesor.apellidos = data['apellidos']

        activo = data['activo']
        if activo is not None:
            profesor.activo = activo

        try:
            profesor.guardar()
        except Exception:
            return ({'message': 'No se pudo resolver su petición.'}, 500)

        return (profesor.obtener_datos(), 201)
