from sqlalchemy import create_engine
from app.core.config import get_settings
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.db.base import Base  # ton Base contenant tous les modèles
from app.models.user import User  # Importer tous les modèles pour s'assurer qu'ils sont enregistrés dans Base

settings = get_settings()
print("Engine va se connecter à :", settings.DATABASE_URL)  # debug

engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(bind=engine)

def admin_app():
    
    db: Session = SessionLocal()
    
    admin_email = "admin@talentia.com"
    if not db.query(User).filter(User.email == admin_email).first():
        admin = User(
            nom="Admin",
            prenom="Talentia",
            email=admin_email,
            password=hash_password("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        print("Utilisateur admin créé avec l'email :", admin_email)
    db.close()


if __name__ == "__main__":
    admin_app()