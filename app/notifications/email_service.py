from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

async def send_reset_password_email(email: str, reset_token: str):
    """Envoie l'email de réinitialisation de mot de passe"""
    try:
        # URL de reset (à adapter selon votre frontend)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        # Construction de l'email
        subject = "Talentia AI - Réinitialisation de votre mot de passe"
        
        html_content = f"""
        <html>
            <body>
                <h2>Réinitialisation de mot de passe</h2>
                <p>Vous avez demandé la réinitialisation de votre mot de passe Talentia AI.</p>
                <p>Cliquez sur le lien ci-dessous pour créer un nouveau mot de passe :</p>
                <a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Réinitialiser mon mot de passe
                </a>
                <p>Ce lien expirera dans 1 heure.</p>
                <p>Si vous n'avez pas fait cette demande, ignorez cet email.</p>
            </body>
        </html>
        """
        
        # Configuration SMTP
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))
        
        # Envoi (exemple avec Gmail)
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Reset password email sent to {email}")
        
    except Exception as e:
        logger.error(f"Failed to send reset password email: {str(e)}")
        raise