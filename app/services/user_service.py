from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    def get_user(db: Session, user_id: int):
        try:
            return db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Erreur de base de données pour user_id {user_id}: {e}")
            return None

    @staticmethod
    def update_user(db: Session, user_id: int, nom: str = None, prenom: str = None):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            if nom:
                user.nom = nom
            if prenom:
                user.prenom = prenom

            db.commit()
            db.refresh(user)
            return user
        except SQLAlchemyError as e:
            logger.error(f"Erreur de mise à jour pour user_id {user_id}: {e}")
            return None
