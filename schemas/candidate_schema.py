"""
Schemas Pydantic para la entidad "Candidate" (candidato).

Este módulo define las estructuras de validación y serialización que usa FastAPI
para recibir y devolver datos relacionados con candidatos.

Clases públicas:
- CandidateBase: campos comunes a los esquemas de candidato (entrada y salida).
- CandidateCreate: esquema de entrada para crear un candidato (hereda de CandidateBase).
- CandidateResponse: esquema de respuesta que incluye el id, número de votos y un mensaje opcional.
- CandidateResponse: esquema de respuesta para los metodos Get que incluye el id,pero sin el campo de mensaje.
"""
from pydantic import BaseModel

class CandidateBase(BaseModel):
    """
    Esquema base con los campos básicos de un candidato.

    Atributos:
    - name (str): Nombre del candidato.
    - party (str | None): Nombre del partido o agrupación (opcional).
    """
    name: str
    party: str | None = None

class CandidateCreate(CandidateBase):
    """
    Esquema de entrada para crear un candidato.
    """
    pass

class CandidateResponse(CandidateBase):
    """ 
    Esquema de respuesta usado cuando la API inserta la información de un candidato.
    """
    id: int
    votes: int
    message: str | None = None
    class Config:
        from_attributes = True
class CandidateResponseGet(BaseModel):
    """ 
    Esquema de respuesta usado cuando la API consulta la información de uno o todos los candidatos.
    """
    id: int
    name: str
    party: str | None = None
    votes: int
    class Config:
        from_attributes = True
