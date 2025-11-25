"""
Schemas Pydantic para la entidad "Voter" (votante).

Este módulo define los modelos de validación y serialización usados por FastAPI
al recibir y devolver datos relacionados con votantes.

Clases definidas:
- VoterBase: campos comunes a los esquemas de votante.
- VoterCreate: esquema para la creación de un votante.
- VoterResponse: esquema devuelto tras operaciones que
  incluye estado sobre si el votante ha votado y un mensaje opcional.
- VoterResponseGet: esquema usado al recuperar un votante (incluye id y estado).
"""
from pydantic import BaseModel

class VoterBase(BaseModel):
    """
    Esquema base con los campos básicos de un votante.

    Atributos:
    - name (str): Nombre completo del votante.
    - email (EmailStr): Correo electrónico del votante.
    """
    name: str
    email: str

class VoterCreate(VoterBase):
    """
    Esquema de entrada para crear un votante.

    Hereda los campos de VoterBase. Se mantiene separado para permitir
    futuras extensiones.
    """
    pass
class VoterResponse(VoterBase):
    """
    Esquema de respuesta usado cuando la API inserta la información de un votante

    Atributos adicionales:
    - has_voted (bool): Indica si el votante ya emitió su voto.
    - message (str | None): Campo opcional para mensajes de confirmación o info.
    """
    has_voted: bool
    message: str | None = None
    class Config:
        from_attributes = True
class VoterResponseGet(VoterBase):
    """
    Esquema usado al recuperar los votantes.
    
    Campos:
    - id (int): Identificador único del votante en la base de datos.
    - has_voted (bool): Indica si el votante ya votó.
    """
    id: int
    has_voted: bool
    class Config:
        from_attributes = True
