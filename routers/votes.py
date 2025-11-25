"""
Módulo de rutas para la entidad "Vote" (voto) en la API.

Este módulo define las rutas y la lógica asociada para manejar las operaciones
relacionadas con los votos, incluyendo la creación de votos, la consulta de
votos y la obtención de estadísticas de votación.

Rutas definidas:
- POST /votes/ : Crea un nuevo voto.
- GET /votes/ : Lista todos los votos registrados.
- GET /votes/statistics : Obtiene estadísticas de votación.

Dependencias:
- FastAPI: para la creación de la API.
- SQLAlchemy: para la interacción con la base de datos.
- Schemas Pydantic: para la validación de datos de entrada y salida.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.vote import Vote
from models.voter  import Voter
from models.candidate import Candidate
from schemas.votes_schema import VoteCreate,VotesResponse,VotesResponseGet

router = APIRouter(prefix="/votes", tags=["Votes"])

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
            ,response_model= VotesResponse
            ,summary="Genera un nuevo voto"
            ,description="""Crea un nuevo voto verificando que no existan los votantes o candidatos
            ,adicional vefica que el votante no haya votado anteriormente.
            """
            ,responses={200: {"description": "datos del voto registrado con el mensaje: Voto registrado exitosamente"}
                        ,404: {"description": "El votante ya votó anteriormente"
                              ,"content":{"application/json":{"example":{"detail":"El votante ya votó anteriormente"}}}}})
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo voto en la base de datos.

    Verifica que el votante y el candidato existan y que el votante no haya votado
    previamente. Registra el voto y actualiza el estado del votante y el conteo de
    votos del candidato.

    Parámetros:
    - vote: Objeto VoteCreate que contiene la información del voto.
    - db: Sesión de base de datos.

    Retorna:
    - VotesResponse: Información del voto registrado.
    """
    #tomar información de votante
    voter = db.query(Voter).get(vote.voter_id)
    if not voter:
        raise HTTPException(404, "El votante no está registrado")

    if voter.has_voted:
        raise HTTPException(404, "El votante ya votó anteriormente")

    #Tomar información de candidato
    candidate = db.query(Candidate).get(vote.candidate_id)
    if not candidate:
        raise HTTPException(404, "No existe candidato ")

    # Registrar voto
    db_vote = Vote(**vote.dict())
    db.add(db_vote)

    # Actualizar estado del votante
    voter.has_voted = True

    #Aumenta el conteo de votos para el candidato
    candidate.votes += 1

    db.commit()
    db.refresh(db_vote)
    #return db_vote
    return VotesResponse(
        id=db_vote.id,
        voter_id=db_vote.voter_id,
        candidate_id=db_vote.candidate_id,
        message="Voto registrado exitosamente"
    )

@router.get("/"
            ,response_model= list[VotesResponseGet]
            ,summary="Listar votos"
            ,description="Se consultan todos los votos registrados en el sistema."
            ,responses={200: {"description": "Lista de votos"},
                        404: {"description": "No se han realizado votos todavía"
                              ,"content":{"application/json":{"example":{"detail":"No se han realizado votos todavía"}}}}})
def list_votes(db: Session = Depends(get_db)):
    """
    Lista todos los votos registrados en la base de datos.

    Parámetros:
    - db: Sesión de base de datos.

    Retorna:
    - list[VotesResponseGet]: Lista de todos los votos registrados.
    """
    votos = db.query(Vote).count()
    if votos==0:
        raise HTTPException(404, "No se han realizado votos todavía")
    return db.query(Vote).all()

@router.get("/statistics"
            ,summary="Estadísticas de votación"
            ,description="Se consultan las estadísticas de votación, incluyendo el total de votos por candidato y el porcentaje de votos."
            ,responses={200: {"description": "Estadísticas de votación"}})
def statistics(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas de votación, incluyendo el total de votos por candidato
    y el porcentaje de votos.

    Parámetros:
    - db: Sesión de base de datos.

    Retorna:
    - dict: Resultados de las estadísticas de votación.
    """
    candidates = db.query(Candidate).all()
    total_votes = db.query(Voter).filter(Voter.has_voted == True).count()

    stats = []
    total_votes = sum(c.votes for c in candidates)

    for c in candidates:
        percentage = (c.votes / total_votes * 100)
        stats.append({
            "Candidato": c.name,
            "Partido": c.party,
            "Votos": c.votes,
            "Porcentaje": f'{round(percentage)} %'
        })

    return {
        "Resultados": stats
        ,"Total Votantes": total_votes
    }
