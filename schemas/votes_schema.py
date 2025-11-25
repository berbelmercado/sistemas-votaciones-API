"""
Schemas Pydantic para la entidad "Vote" (voto).

Este módulo define las estructuras de datos usadas por FastAPI para validar
entrada y salida relacionadas con votos.

Clases:
- VoteBase: campos comunes para un voto.
- VoteCreate: esquema para crear un voto (hereda de VoteBase).
- VotesResponse: esquema de respuesta que incluye el id del recurso y un
  campo opcional de mensaje.
-VotesResponseGet: esquema usado al recuperar votos incluye id y elimina mensaje.
"""
from pydantic import BaseModel

class VoteBase(BaseModel):
    """
    Esquema base que contiene los campos mínimos que identifican un voto.

    Atributos:
    - id (int): Identificador único del voto.
    - voter_id (int): ID del votante que emite el voto.
    - candidate_id (int): ID del candidato que recibe el voto.
    """
    voter_id: int
    candidate_id: int

class VoteCreate(VoteBase):
    """
    Esquema usado al crear un voto a través de la API.
    """
    pass

class VotesResponse(BaseModel):
    """
    Esquema usado en las respuestas que devuelven al crear un nuevo voto.

    Atributos:
    - id (int): Identificador único del voto en la base de datos.
    - voter_id (int): ID del votante (heredado).
    - candidate_id (int): ID del candidato (heredado).
    . message (str | None): Mensaje opcional adicional.
    """
    id: int
    voter_id: int
    candidate_id: int
    message: str | None = None
    class Config:
        from_attributes = True

class VotesResponseGet(BaseModel):
    """
    Esquema usado en las respuestas que devuelven los votos almacenados.

    Atributos:
    - id (int): Identificador único del voto en la base de datos.
    - voter_id (int): ID del votante (heredado).
    - candidate_id (int): ID del candidato (heredado).
    . message (str | None): Mensaje opcional adicional.
    """
    id: int
    voter_id: int
    candidate_id: int

    class Config:
        from_attributes = True
