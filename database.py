"""
database.py
-----------
Configuración central de acceso a base de datos para el proyecto.

Este módulo encapsula la configuración mínima necesaria para usar SQLAlchemy
con una base de datos SQLite localizada en el directorio 'databases' del
proyecto.

Elementos exportados:
- DATABASE_URL: cadena de conexión usada por SQLAlchemy.
- engine: motor creado por create_engine.
- SessionLocal: fábrica de sesiones para obtener sesiones DB.
- Base: clase base declarativa para definir modelos ORM.
- get_db: generador/context manager recomendado para obtener y liberar sesiones
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cadena de conexión: usa SQLite ubicado en la carpeta 'databases' del proyecto.
DATABASE_URL = "sqlite:///databases/votaciones.db"

#Para permitir multiples hilos
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base declarativa, padre para los modelos
Base = declarative_base()