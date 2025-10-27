from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Enum as SQLEnum
import enum
from datetime import datetime, timedelta
import uuid

class UserRole(str, enum.Enum):
   ADMIN = "admin"
   CANDIDAT = "candidat"
   RECRUTEUR = "recruteur"


class User(Base):

   __tablename__ = "users"
   id = Column(Integer, autoincrement=True, primary_key=True, index=True)
   nom = Column(String(100), nullable=False)
   prenom = Column(String(100), nullable=False)
   email = Column(String(100), unique=True, index=True, nullable=False)
   password = Column(String(255), nullable=False)
   role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CANDIDAT, nullable=False)
   est_actif = Column(Boolean, default=True)

   #les champs pour la reinitialisation de mot de passe

   reset_token = Column(String(255), nullable=True, index=True)
   reset_token_expires = Column(DateTime, nullable=True)

   def generate_reset_token(self):
      self.reset_token = str(uuid.uuid4())
      self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
      return self.reset_token
   

   def is_reset_token_valid(self):
        return (self.reset_token is not None and 
                self.reset_token_expires > datetime.utcnow())

    
   def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expires = None

   def __repr__(self):
      return f"<User(id={self.id}, email={self.email}, nom={self.nom}, prenom={self.prenom})>"
