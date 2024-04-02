"""
Modelo alumno
"""
from datetime import datetime
from datetime import timezone
from typing import Optional

from sqlalchemy import TIMESTAMP
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import expression

from aplicacion.db import db
from aplicacion.helpers.utilidades import Utilidades


class AlumnoModel(db.Model):
    """
    Modelo alumno
    """
    __tablename__ = 'alumno'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    nombres: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(100))
    rut: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    fecha_inscripcion: Mapped[float] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc)
    )
    activo: Mapped[bool] = mapped_column(default=expression.true())

    def __init__(
            self,
            nombres: str,
            apellidos: str,
            rut: str,
            fecha_inscripcion: Optional[datetime] = None,
            inactive: bool = False
    ):
        self.nombres = nombres
        self.apellidos = apellidos
        self.rut = rut
        if fecha_inscripcion:
            self.fecha_inscripcion = fecha_inscripcion.timestamp()
        if inactive:
            self.activo = False

    def obtener_datos(self):
        """
        Entrega los datos como diccionario
        """
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'rut': self.rut,
            'fecha_inscripcion': Utilidades.formato_fecha(self.fecha_inscripcion),
            'activo': self.activo
        }

    @classmethod
    def buscar_por_rut(cls, rut):
        """
        Busca el alumno mediante el rut
        """
        return cls.query.filter_by(rut=rut).first()

    @classmethod
    def buscar_existencia(cls, rut: str) -> Optional['AlumnoModel']:
        """
        Busca si existe el alumno
        """
        return cls.query.filter_by(rut=rut).first()

    def guardar(self):
        """
        Guarda el alumno
        """
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        """
        Elimina el alumno
        """
        db.session.delete(self)
        db.session.commit()
