from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserOut
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db
from app.schemas.user import ForgotPasswordRequest
from app.schemas.user import ResetPasswordResponse
from app.schemas.user import ResetPasswordRequest
from app.models.user import User, UserRole
from app.services.auth_service import AuthService 
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email déjà utilisé")

    # Hasher le mot de passe
    hashed_password = hash_password(user.password)

    # Créer l'utilisateur avec le rôle fourni
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        password=hashed_password,
        role=user.role  # <-- important pour que le rôle soit enregistré
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur non trouvé")

    # Vérifier le mot de passe
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Mot de passe incorrect")

    # Générer le token JWT
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Initie la réinitialisation du mot de passe
    """
    success = await AuthService.forgot_password(db, request.email)
    
    # Toujours retourner success=True pour la sécurité
    return {
        "message": "Si l'email existe, un lien de réinitialisation a été envoyé.",
        "success": True
    }

@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Réinitialise le mot de passe avec le token
    """
    success = await AuthService.reset_password(db, request.token, request.new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token invalide ou expiré"
        )
    
    return ResetPasswordResponse(
        message="Mot de passe réinitialisé avec succès",
        success=True
    )
