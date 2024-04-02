"""
alumnos Module
"""
from flask_restful import Resource
from flask_restful import reqparse

from aplicacion.modelos.alumno import AlumnoModel


class Alumnos(Resource):
    """
    a
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'nombres',
        type=str,
        required=True,
        help='Debe ingresar un nombre para el alumno'
    )
    parser.add_argument(
        'apellidos',
        type=str,
        required=True,
        help='Debe ingresar un apellido para el alumno.'
    )
    parser.add_argument(
        'rut',
        type=str,
        required=True,
        help='Debe ingresar un rut para el alumno.'
    )
    parser.add_argument(
        'activo',
        type=bool,
        required=False,
        choices=(True, False),
        help='Debe ingresar 0 para estado inactivo y 1 para estado activo.'
    )

    def get(self):
        """
        Entrega la lista de alumnos.
        ---
        tags:
          - alumnos
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'alumnos': []}
        """
        return {'alumnos': list(map(lambda x: x.obtener_datos(), AlumnoModel.query.all()))}

    def post(self):
        """
        Guardar alumno
        ---
        tags:
          - alumnos
        parameters:
          - name: alumnos
            in: body
            schema:
                type: object
                required:
                - nombres
                - apellidos
                - rut
                - activo
                properties:
                    nombres:
                        type: string
                        maxLength: 80
                    apellidos:
                        type: string
                        maxLength: 80
                    rut:
                        type: string
                        maxLength: 15
                    activo:
                        type: boolean
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {
                        'alumno': {
                            'id': 1,
                            'nombres': 'jose juan',
                            'apellidos': 'vicuña muñoz',
                            'fecha_inscripcion': '12-10-19',
                            'activo': true
                        }
                    }
        """
        data = Alumnos.parser.parse_args()
        rut = str(data['rut'])

        if AlumnoModel.buscar_existencia(rut):
            return (
                {'message': f'Ya existe un alumno llamado \'{data["nombres"]} {data["apellidos"]}\''
                            f' con rut: {data["rut"]}'},
                400
            )

        inactive = (not data['activo']) if data['activo'] else False
        alumno = AlumnoModel(data['nombres'], data['apellidos'], rut, inactive=inactive)

        try:
            alumno.guardar()
        except Exception as e:
            return ({'message': f'No se pudo resolver su petición. {e}'}, 500)
        return (alumno.obtener_datos(), 201)

    def put(self):
        """
        Guardar alumno
        ---
        tags:
          - alumnos
        parameters:
          - name: alumnos
            in: body
            schema:
                type: object
                required:
                - nombres
                - apellidos
                - rut
                properties:
                    nombres:
                        type: string
                        maxLength: 80
                    apellidos:
                        type: string
                        maxLength: 80
                    rut:
                        type: string
                        maxLength: 15
        responses:
            200:
                description: Respuesta exitosa.
                examples:
                    application/json: {'alumnos': []}
        """
        data = Alumnos.parser.parse_args()
        alumno_nombres = data['nombres']
        alumno_apellidos = data['apellidos']
        alumno_rut = data['rut']
        activo = data['activo']

        alumno = AlumnoModel.buscar_existencia(
            alumno_rut
        )

        if not alumno:
            return ({'message': 'No se pudo resolver su petición.'}, 400)

        # Cambiar los datos.
        alumno.nombres = alumno_nombres or alumno.nombres
        alumno.apellidos = alumno_apellidos or alumno.apellidos
        alumno.rut = alumno_rut or alumno.rut

        if activo is not None:
            alumno.activo = activo

        try:
            alumno.guardar()
        except Exception:
            return ({'message': 'No se pudo resolver su petición.'}, 500)
        return (alumno.obtener_datos(), 201)
