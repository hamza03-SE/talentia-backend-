from sqlalchemy import create_engine
import app.core.config
from sqlalchemy.orm import sessionmaker

settings = app.core.config.get_settings()
engine = create_engine(
    settings.DATABASE_URL,  
    pool_pre_ping=True
    )
                                  

SessionLocal = sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

