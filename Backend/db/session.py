from sqlalchemy.orm import sessionmaker
from db.database import engine, Base

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Este es get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
