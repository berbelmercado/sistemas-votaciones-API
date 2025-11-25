"""
Modelo SQLAlchemy para la entidad "Candidate" (candidato).

Este módulo define la estructura de la tabla "candidates" en la base de datos
y su relación con la entidad "Vote".

Uso:
- Importar la clase Candidate en routers o en lógica de negocio para realizar
  operaciones CRUD usando una sesión SQLAlchemy.

Atributos de la tabla:
- id (Integer, PK): Identificador único del candidato.
- name (String, not null): Nombre del candidato.
- party (String, nullable): Partido o agrupación política (opcional).
- votes (Integer, default=0): Contador de votos acumulados para el candidato.

Relaciones:
- votes_rel: Relación hacia la tabla de votos (modelo Vote). Permite acceder a
  todos los objetos Vote asociados con este candidato mediante ORM.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Candidate(Base):
    """
    Clase ORM que representa la tabla 'candidates'.

    Propiedades:
    - id: clave primaria auto incremental, índice para búsquedas.
    - name: nombre del candidato; requerido.
    - party: partido o afiliación; opcional.
    - votes: contador de votos (entero) inicializado a 0.
    - votes_rel: relación ORM (lista) hacia objetos Vote asociados.
    """
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    votes = Column(Integer, default=0)

    votes_rel = relationship("Vote", back_populates="candidate")
