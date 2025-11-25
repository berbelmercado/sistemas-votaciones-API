"""
Módulo de rutas para la entidad "Voter" (votante) en la API.

Este módulo define las rutas y la lógica asociada para manejar las operaciones
relacionadas con los votantes, incluyendo el registro, consulta, listado y eliminación
de votantes.

Rutas definidas:
- POST /voters/ : Registra un nuevo votante.
- GET /voters/ : Lista todos los votantes registrados.
- GET /voters/{id} : Consulta un votante por su ID.
- DELETE /voters/{id} : Elimina un votante por su ID.

Dependencias:
- FastAPI: para la creación de la API.
- SQLAlchemy: para la interacción con la base de datos.
- Schemas Pydantic: para la validación de datos de entrada y salida.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.voter import Voter
from models.candidate import Candidate
from schemas.voter_schema import VoterResponse, VoterCreate, VoterResponseGet

router = APIRouter(prefix="/voters", tags=["Voters"])

def get_db():
    """
    Dependencia para obtener una sesión de base de datos.

    Crea una nueva sesión de base de datos y la cierra al finalizar la operación.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/"
             ,response_model=VoterResponse
             ,summary="Registrar un nuevo votante"
             ,description="""Crea un nuevo votante verificando que no exista un votante con el mismo correo
             ni un candidato con el mismo nombre."""
             ,responses={404: {"description": "Correo ya registrado o nombre ya existe como candidato"
                              ,"content":{"application/json":{"example":{"detail":"Este correo ya está registrado."}}}}}
                        )
def create_voter(voter: VoterCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo votante en la base de datos.

    Verifica que no exista un votante con el mismo correo electrónico y que el nombre
    no esté registrado como candidato. Si se encuentra un duplicado, se lanza una excepción.

    Parámetros:
    - voter: Objeto VoterCreate que contiene la información del votante.
    - db: Sesión de base de datos.

    Retorna:
    - VoterResponse: Información del votante registrado.
    """
    # Validar email duplicado
    email_exists = db.query(Voter).filter(Voter.email == voter.email).first()
    # Validar que no exista como candidato
    candidate_exists = db.query(Candidate).filter(Candidate.name == voter.name).first()

    if email_exists:
        raise HTTPException(404, "Este correo ya está registrado.")
    if candidate_exists:
        raise HTTPException(404, "Este usuario ya está registrado como candidato.")

    db_voter = Voter(**voter.dict())
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)

    return VoterResponse(
        id=db_voter.id,
        name=db_voter.name,
        email=db_voter.email,
        has_voted=db_voter.has_voted,
        message="Votante registrado exitosamente"
    )

@router.get("/"
            ,response_model=list[VoterResponseGet]
            ,summary="Listar votantes"
            ,description="""Se consultan todos los votantes registrados en el sistema.
            Si no hay votantes registrados, se retorna un error 404."""
            ,responses={200: {"description": "Lista de votantes"},
                        404: {"description": "No hay votantes registrados"
                              ,"content":{"application/json":{"example":{"detail":"No hay votantes registrados"}}}}})
def list_voters(db: Session = Depends(get_db)):
    """
    Lista todos los votantes registrados en la base de datos.

    Parámetros:
    - db: Sesión de base de datos.

    Retorna:
    - list[VoterResponseGet]: Lista de todos los votantes registrados.
    """
    cantidad = db.query(Voter).count()#obtenemos la cantidad de votos registrados
    if cantidad ==0:
        raise HTTPException(404, "No hay votantes registrados")
    return db.query(Voter).all()

@router.get("/{id}"
            ,response_model=VoterResponseGet
            ,summary="Consultar votante por Id"
            ,description="""Se consultan un votante con su número de Id. si no existe, se retorna un error 404."""
            ,responses={404: {"description": "No se encontró votante"
                              ,"content":{"application/json":{"example":{"detail":"No se encontró votante"}}}
                              }}
            )
def get_voter(id: int, db: Session = Depends(get_db)):
    voter = db.get(Voter, id) #Se consulta la información en la bd
    if not voter:
        raise HTTPException(404, "No se encontró votante")
    return voter

@router.delete("/{id}"
               ,summary="Eliminar votante por Id"
               ,description="""Elimina un votante con su número de Id. si no existe, se retorna un error 404."""
               ,responses={200: {"description": "Votante eliminado"
                                 ,"content":{"application/json":{"example":{"message":"Votante eliminado"}}}},
                          404: {"description": "No se encontró votante para eliminar"
                                ,"content":{"application/json":{"example":{"detail":"No se encontró votante para eliminar"}}}}})
def delete_voter(id: int, db: Session = Depends(get_db)):
    """
    Consulta un votante por su ID.

    Parámetros:
    - id: Identificador único del votante.
    - db: Sesión de base de datos.

    Retorna:
    - VoterResponseGet: Información del votante encontrado.
    """
    voter = db.query(Voter).get(id)
    if not voter:
        raise HTTPException(404, "No se encontró votante para eliminar")
    db.delete(voter)
    db.commit()
    return {"message": "Votante eliminado"}
