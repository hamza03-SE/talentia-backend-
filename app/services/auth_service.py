# app/services/auth_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from app.notifications.email_service import send_reset_password_email
import logging

logger = logging.getLogger(__name__)

class AuthService:
    
    @staticmethod
    async def forgot_password(db: Session, email: str) -> bool:
        """Génère et envoie le token de reset password"""
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                # Pour la sécurité, on ne révèle pas si l'email existe
                logger.info(f"Password reset requested for non-existent email: {email}")
                return True
            
            # Générer le token
            reset_token = user.generate_reset_token()
            db.commit()
            
            # Envoyer l'email
            await send_reset_password_email(user.email, reset_token)
            
            logger.info(f"Reset password email sent to: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error in forgot_password: {str(e)}")
            return False
    
    @staticmethod
    async def reset_password(db: Session, token: str, new_password: str) -> bool:
        """Réinitialise le mot de passe avec le token"""
        try:
            user = db.query(User).filter(User.reset_token == token).first()
            
            if not user or not user.is_reset_token_valid():
                return False
            
            #  Hasher et enregistrer le nouveau mot de passe
            user.password = hash_password(new_password)

            # Supprimer le token de réinitialisation
            user.clear_reset_token()

            db.commit()
            db.refresh(user)
            
            logger.info(f"Password reset successfully for user: {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error resetting password: {str(e)}")
            return False
