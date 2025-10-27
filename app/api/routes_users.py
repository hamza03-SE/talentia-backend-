from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from app.dependencies import get_current_user 
from app.db.session import get_db
from app.schemas.user import UserUpdate
from app.services.user_service import UserService 
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)

def get_profile(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user = UserService.get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouve")
    return user

@router.put("/update", response_model=UserOut)
def update_profile(update: UserUpdate, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    user = UserService.update_user(db, current_user.id, update.nom, update.prenom)

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouve")
    return user

