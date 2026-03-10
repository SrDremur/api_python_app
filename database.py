from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import platform

# Cargamos variables de entorno desde un archivo .env
load_dotenv()

# Estructura: postgresql://usuario:password@localhost:5432/nombre_db
# Para Supabase usarás la URL que te dan en su panel de Settings -> Database
DATABASE_URL = os.getenv("DATABASE_URL")

if platform.system() == "Windows" or not DATABASE_URL:
    DATABASE_URL = "postgresql+psycopg://productos_db_afso_user:yfCUdhuhG4lN2h8MRIeLOwbJGMlvfXSD@dpg-d6ni9uhaae7s73c0n8q0-a.oregon-postgres.render.com/productos_db_afso"

# 3. Corrección para Render (por si acaso envían postgres://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
# 4. Aseguramos que siempre use el driver psycopg
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
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