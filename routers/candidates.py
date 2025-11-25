"""
Rutas y lógica para la entidad "Candidate" (candidato).

Responsabilidades:
- Exponer endpoints CRUD para candidatos.
- Validar colisiones de datos con votantes/candidatos existentes.
- Proveer respuestas claras y códigos HTTP apropiados.

Endpoints:
- POST /candidates/        -> Crear un nuevo candidato.
- GET  /candidates/        -> Listar todos los candidatos.
- GET  /candidates/{id}    -> Obtener un candidato por id.
- DELETE /candidates/{id}  -> Eliminar un candidato por id.

"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.voter import Voter
from models.candidate import Candidate
from schemas.candidate_schema import CandidateCreate, CandidateResponse,CandidateResponseGet

router = APIRouter(prefix="/candidates", tags=["Candidates"])

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

@router.post("/",response_model=CandidateResponse
             ,summary="Registrar un nuevo candidato"
             ,description="""Crea un nuevo candidato verificando que no exista un votante o candidato con el mismo nombre."""
             ,responses={200: {"description": "datos del candidato registrado con el mensaje: Candidato registrado exitosamente"},
                        404: {"description": "Nombre ya existe como votante o candidato"
                              ,"content":{"application/json":{"example":{"detail":"Este usuario ya está registrado como votante."}}}}}
                        )
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo candidato en la base de datos.

    Validaciones:
    - Si ya existe un votante con el mismo nombre -> 404
    - Si ya existe un candidato con el mismo nombre -> 404

    Parámetros:
    - candidate: CandidateCreate (datos de entrada).
    - db: Sesión de base de datos proporcionada por get_db.

    Devuelve:
    - CandidateResponse con los campos del candidato creado y un mensaje.
    """
    voter_exists = db.query(Voter).filter(Voter.name == candidate.name).first()
    candidate_exists = db.query(Candidate).filter(Candidate.name == candidate.name).first()
    if voter_exists:
        raise HTTPException(404, "Este usuario ya está registrado como votante.")
    if candidate_exists:
        raise HTTPException(404,"Esta candidato ya está registrado.")
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    return CandidateResponse(
        id=db_candidate.id,
        name=db_candidate.name,
        party=db_candidate.party,
        votes=db_candidate.votes,
        message="Candidato registrado exitosamente"
    )

@router.get("/",response_model=list[CandidateResponseGet]
            ,summary="Listar candidatos"
            ,description="Se consultan todos los candidatos registrados en el sistema."
            ,responses={200: {"description": "Lista de candidatos"},
                        404: {"description": "No hay candidatos registrados"
                              ,"content":{"application/json":{"example":{"detail":"No hay candidatos registrados"}}}}})
def list_candidates(db: Session = Depends(get_db)):
    """
    Recupera la lista de candidatos.

    Si no hay candidatos registrados se lanza HTTPException(404).

    Devuelve:
    - Lista de CandidateResponseGet.
    """
    candidates = db.query(Candidate).count()
    if candidates ==0:
        raise HTTPException(404, "No hay candidatos registrados")
    return db.query(Candidate).all()

@router.get("/{id}",response_model=CandidateResponseGet
            ,summary="Consultar candidato por Id"
            ,description="Se consultan un candidato con su número de Id."
            ,responses={200: {"description": "Datos del candidato"},
                        404: {"description": "Candidato no encontrado"
                              ,"content":{"application/json":{"example":{"detail":"Candidato no encontrado"}}}}})
def get_candidate(id: int, db: Session = Depends(get_db)):
    """
    Busca un candidato por id.

    Parámetros:
    - id: int, identificador del candidato.
    - db: Sesión de base de datos.

    Devuelve:
    - CandidateResponseGet si existe, si no -> HTTPException(404).
    """
    candidate = db.query(Candidate).get(id)
    if not candidate:
        raise HTTPException(404, "Candidato no encontrado")
    return candidate

@router.delete("/{id}"
               ,summary="Eliminar candidato por Id"
               ,description="Elimina un candidato con su número de Id."
               ,responses= {200: {"description": "Candidato eliminado"
                                 ,"content":{"application/json":{"example":{"message":"Candidato eliminado"}}}},
                            404: {"description": "Candidato no encontrado"
                                ,"content":{"application/json":{"example":{"detail":"Candidato no encontrado"}}}}})
def delete_candidate(id: int, db: Session = Depends(get_db)):
    """
    Elimina un candidato por id.

    Parámetros:
    - id: int, identificador del candidato.
    - db: Sesión de base de datos.

    Comportamiento:
    - Si no existe el candidato -> HTTPException(404)
    - Si existe -> elimina y confirma con un mensaje JSON.
    """
    candidate = db.query(Candidate).get(id)
    if not candidate:
        raise HTTPException(404, "Candidato no encontrado")
    db.delete(candidate)
    db.commit()
    return {"message": "Candidato eliminado"}
