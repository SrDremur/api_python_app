from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Cargamos variables de entorno desde un archivo .env
load_dotenv()

# Estructura: postgresql://usuario:password@localhost:5432/nombre_db
# Para Supabase usarás la URL que te dan en su panel de Settings -> Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://productos_db_afso_user:yfCUdhuhG4IN2h8MRleL0wbJGMlvfxSD@dpg-d6ni9uhaae7s73c0n8q0-a/productos_db_afso")

# El motor de conexión (Engine)
# Usamos el driver 'psycopg' (el 3) que es el que definiste en tu stack
engine = create_engine(DATABASE_URL)

# La fábrica de sesiones para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para crear tus modelos
Base = declarative_base()

# Dependencia para FastAPI: abre la conexión y la cierra al terminar la petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()