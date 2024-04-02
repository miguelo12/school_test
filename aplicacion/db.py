"""
Configuración para flask_sqlalchemy
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """
    Clase base de los modelos
    """
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())


db = SQLAlchemy(model_class=Base)
