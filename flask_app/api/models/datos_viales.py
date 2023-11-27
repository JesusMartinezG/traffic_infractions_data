from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Double
from sqlalchemy.orm import Mapped, mapped_column
from flask_app.database import db

class inviales (db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    folio:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    creacion:Mapped[datetime] = mapped_column(DateTime)
    dia_semana:Mapped[str] = mapped_column(String)
    cierre:Mapped[datetime] = mapped_column(DateTime)
    tipo_incidente_c4:Mapped[str] = mapped_column(String)
    incidente_c4:Mapped[str] = mapped_column(String)
    alcaldia_inicio:Mapped[str] = mapped_column(String)
    latitud:Mapped[float] = mapped_column(Double)
    longitud:Mapped[float] = mapped_column(Double)
    codigo_cierre:Mapped[str] = mapped_column(String)
    clas_con_f_alarma:Mapped[str] = mapped_column(String)
    tipo_entrada:Mapped[str] = mapped_column(String)
    alcaldia_cierre:Mapped[str] = mapped_column(String)
    colonia:Mapped[str] = mapped_column(String)