"""
app.py
------
Punto de entrada de la API "Sistema de Votaciones".

Responsabilidades principales:
- Crear las tablas en la base de datos a partir de los modelos declarativos.
- Instanciar la aplicación FastAPI y centralizar metadata (título, descripción).
- Registrar (incluir) los routers que exponen los endpoints para votantes,
  candidatos y votos.

Dependencias del workspace:
- Base (declarative_base) y engine (sqlalchemy) en database.py:
  -> [`Base`](database.py), [`engine`](database.py)
- Routers con los endpoints:
  -> Voters: [`router`](routers/voter.py) en [routers/voter.py](routers/voter.py)
  -> Candidates: [`router`](routers/candidates.py) en [routers/candidates.py](routers/candidates.py)
  -> Votes: [`router`](routers/votes.py) en [routers/votes.py](routers/votes.py)

Notas de despliegue:
- La configuración de conexión está en database.py. Para desarrollo local usa
  el fichero SQLite en databases/votaciones.db .
"""
from fastapi import FastAPI
from database import Base, engine
from routers import voter, candidates,votes

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Votaciones",
            description="""API para gestionar votantes, candidatos y votos.
            Incluye endpoints para crear votantes, emitir votos y consultar resultados.
            """)

app.include_router(voter.router)
app.include_router(candidates.router)
app.include_router(votes.router)