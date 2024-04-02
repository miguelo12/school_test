"""
Modelo usuarioBusca el profesor mediante el rut
"""
from typing import Dict
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import expression

from aplicacion.db import db


class UsuarioModel(db.Model):
    """
    Modelo usuario
    """
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    salt: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(250))
    activo: Mapped[bool] = mapped_column(default=expression.true())

    def __init__(self, username: str, password: str, salt: str):
        self.username = username
        self.password = password
        self.salt = salt

    def obtener_datos(self) -> Dict:
        """
        Entregas los datos del usuario como un diccionario
        """
        if not self.activo:
            return {}

        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'salt': self.salt,
            'activo': self.activo
        }

    @classmethod
    def buscar_por_id(cls, usuario_id) -> Optional['UsuarioModel']:
        """
        Busca si existe el usuario mediante el usuario_id
        """
        return cls.query.filter_by(id=usuario_id).first()

    @classmethod
    def buscar_username(cls, username: str) -> Optional['UsuarioModel']:
        """
        Busca si existe el usuario mediante el username
        """
        return cls.query.filter_by(username=username).first()

    def guardar(self) -> None:
        """
        Guarda el usuario
        """
        db.session.add(self)
        db.session.commit()

    def eliminar(self) -> None:
        """
        Elimina el usuario
        """
        db.session.delete(self)
        db.session.commit()
