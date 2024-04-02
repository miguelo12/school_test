"""
a
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import expression

from aplicacion.db import db


class ProfesorModel(db.Model):
    """
    Modelo profesor
    """
    __tablename__ = 'profesor'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    nombress: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(100))
    rut: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    activo: Mapped[bool] = mapped_column(default=expression.true())

    def __init__(self, nombres: str, apellidos: str, rut: str):
        self._id = None
        self.nombres = nombres
        self.apellidos = apellidos
        self.rut = rut

    def obtener_datos(self):
        """
        Entrega los datos como diccionario
        """
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'rut': self.rut,
            'activo': self.activo
        }

    @classmethod
    def buscar_por_rut(cls, rut):
        """
        Busca el profesor mediante el rut
        """
        return cls.query.filter_by(rut=rut).first()

    @classmethod
    def buscar_existencia(cls, rut):
        """
        Busca si existe el profesor mediante el rut
        """
        return cls.query.filter_by(nombres=rut).exists().first()

    def guardar(self):
        """
        Guarda el profesor
        """
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        """
        Elimina el profesor
        """
        db.session.delete(self)
        db.session.commit()
