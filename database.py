from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cadena de conexión: usa SQLite ubicado en la carpeta 'databases' del proyecto.
DATABASE_URL = "sqlite:///databases/votaciones.db"

#Para permitir multiples hilos
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
#Manejo de seciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base declarativa, padre para los modelos

Base = declarative_base()
