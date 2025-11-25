"""
Modelo SQLAlchemy para la entidad "Voter" (votante).

Este módulo define la estructura de la tabla de votantes en la base de datos,
así como las relaciones con otras entidades (votos).

Atributos de la clase Voter:
- id: Identificador único del votante.
- name: Nombre completo del votante.
- email: Correo electrónico del votante (debe ser único).
- has_voted: Indica si el votante ha emitido su voto (valor booleano).

Relaciones:
- vote: Relación con el modelo Vote, permite acceder al voto emitido por el votante.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    has_voted = Column(Boolean, default=False)

    vote = relationship("Vote", back_populates="voter", uselist=False)
