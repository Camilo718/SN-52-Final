import os  # Asegúrate de tener esta importación al principio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexión a tu base MySQL
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:admin@localhost:3315/sn-52-3147234'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()