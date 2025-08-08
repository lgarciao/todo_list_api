import time
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.infrastructure.db.base import Base
from app.infrastructure.db import models


# Lee la URL de la base de datos desde una variable de entorno.
# Si no está definida, usa la URL de desarrollo por defecto.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/todo_db")

# Variables para la lógica de reintento
MAX_RETRIES = 5
RETRY_DELAY = 5  # Segundos


# Función para intentar crear el motor de la base de datos con reintentos
def create_database_engine():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print(
                f"Attempting to connect to database... (Attempt {retries + 1}/{MAX_RETRIES})"
            )
            engine = create_engine(DATABASE_URL)

            # Intenta una conexión de prueba para verificar si la base de datos está lista
            with engine.connect():
                print("Database connection successful!")
                return engine
        except OperationalError:
            print(
                f"Database is not ready. Waiting {RETRY_DELAY} seconds before retrying..."
            )
            retries += 1
            time.sleep(RETRY_DELAY)

    # Si todos los reintentos fallan, lanza una excepción
    raise ConnectionError("Failed to connect to the database after multiple retries.")


# Crea el motor de la base de datos usando la función con reintentos
engine = create_database_engine()

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
