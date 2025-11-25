"""
Modelo SQLAlchemy para la entidad "Vote" (voto).

Este módulo define la estructura de la tabla de votos en la base de datos,
así como las relaciones con otras entidades (votantes y candidatos).

Atributos de la clase Vote:
- id: Identificador único del voto.
- voter_id: ID del votante que emite el voto (clave foránea).
- candidate_id: ID del candidato que recibe el voto (clave foránea).

Relaciones:
- voter: Relación con el modelo Voter, permite acceder al votante que emitió el voto.
- candidate: Relación con el modelo Candidate, permite acceder al candidato que recibió el voto.
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))

    voter = relationship("Voter", back_populates="vote")
    candidate = relationship("Candidate", back_populates="votes_rel")