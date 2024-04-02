"""
a
"""
from datetime import datetime
from datetime import timezone
from typing import TYPE_CHECKING
from typing import List

from sqlalchemy import SMALLINT
from sqlalchemy import TIMESTAMP
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from aplicacion.db import db
from aplicacion.helpers.utilidades import Utilidades

if TYPE_CHECKING:
    from aplicacion.modelos.alumno import AlumnoModel
    from aplicacion.modelos.profesor import ProfesorModel

# Se define la tabla que contiene la relación mucho a muchos
# Se aconseja que las tablas intermedias no tengan modelo. No se por qué.
# De todos modos, si se fijan en los modelos agregué esto :
# __table_args__ = {'extend_existing': True}  (linea 27 aprox en este archivo)
# Eso ayudará a que se pueda hacer multiples referencias a la misma tabla
curso_alumno = Table(
    'alumno_curso',
    db.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_curso', Integer, ForeignKey('curso.id'), nullable=False),
    Column('id_alumno', Integer, ForeignKey('alumno.id'), nullable=False)
)


class CursoModel(db.Model):
    """
    Modelo curso
    """
    __tablename__ = 'curso'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    profesor_id: Mapped[int] = mapped_column(ForeignKey('profesor.id'))
    nivel: Mapped[int] = mapped_column(SMALLINT)
    activo: Mapped[bool] = mapped_column(default=expression.true())
    fecha_creacion: Mapped[float] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc)
    )

    # Se crea el objeto profesor
    profesor: Mapped['ProfesorModel'] = relationship(backref='cursos')

    # Se crea el objeto de alumnos.
    alumnos: Mapped[List['AlumnoModel']] = relationship(
        'AlumnoModel',
        secondary=curso_alumno,
        backref='cursos'
    )

    def __init__(
            self,
            nombre: str,
            profesor_id: int,
            nivel: int,
            inactive: bool = False):
        self.nombre = nombre
        self.profesor_id = profesor_id
        self.nivel = nivel

        if inactive:
            self.activo = True

    def obtener_datos(self):
        """
        a
        """
        data_profesor = {
            'id': self.profesor_id,
            'nombres': self.profesor.nombres,
            'apellidos': self.profesor.apellidos
        }
        return {
            'id': self.id,
            'nombre': self.nombre,
            'nivel': self.nivel,
            'activo': self.activo,
            'fecha_creacion': Utilidades.formato_fecha(self.fecha_creacion),
            'profesor': data_profesor
        }

    def obtener_alumnos(self):
        """
        Entrega los datos como diccionario
        """
        data_profesor = {
            'id': self.profesor_id,
            'nombres': self.profesor.nombres,
            'apellidos': self.profesor.apellidos
        }

        lista_alumnos = {}
        for alumno in self.alumnos:
            lista_alumnos[alumno.id] = {
                "nombres": alumno.nombres,
                "apellidos": alumno.apellidos,
                "fecha_inscripcion": Utilidades.formato_fecha(alumno.fecha_inscripcion),
                "activo": alumno.activo
            }

        return {
            'id': self.id,
            'nombre': self.nombre,
            'nivel': self.nivel,
            'activo': self.activo,
            'profesor': data_profesor,
            "alumnos": lista_alumnos
        }

    @classmethod
    def buscar_por_nombre(cls, nombre: str):
        """
        Busca el curso mediante el nombre
        """
        return cls.query.filter_by(nombre=nombre).first()

    @classmethod
    def buscar_existencia(cls, nombre: str):
        """
        Busca si existe el curso mediante el nombre
        """
        return cls.query.filter_by(nombre=nombre).first()

    def guardar(self):
        """
        Guarda el curso
        """
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        """
        Elimina el curso
        """
        db.session.delete(self)
        db.session.commit()
