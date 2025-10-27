from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
from app.models.user import UserRole
import re

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str
    role: Optional[UserRole] = UserRole.CANDIDAT

    # Validation du mot de passe
    @field_validator('password')
    def password_strong(cls, v):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, v):
            raise ValueError(
                'Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.'
            )
        return v

    # Validation du rôle
    @field_validator('role', mode='before')
    def validate_role(cls, v):
        if isinstance(v, str):
            # Normaliser en minuscules
           normalized = v.lower()
           for r in UserRole:
               if r.value == normalized:
                  return r
           raise ValueError(f"Role invalide: {v}. Choisir parmi {[r.value for r in UserRole]}")
        return v

class UserOut(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    role: UserRole
    est_actif: bool

    class Config:
        orm_mode = True  # Pour permettre la conversion depuis les objets ORM




class ForgotPasswordRequest(BaseModel):
    email : EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ResetPasswordResponse(BaseModel):

    message: str
    success: bool


