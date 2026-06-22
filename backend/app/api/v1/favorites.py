from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.constants.enums import FavoriteType
from app.core.database import get_db
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse, FavoriteStatusResponse
from app.services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/toggle", response_model=FavoriteStatusResponse)
def toggle_favorite(payload: FavoriteCreate, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    favorite, is_added = FavoriteService.toggle_favorite(db, user, payload.target_type, payload.target_id, request.client.host if request.client else None)
    return FavoriteStatusResponse(is_favorited=is_added, favorite_id=favorite.id if is_added else None)


@router.get("/status/{target_type}/{target_id}", response_model=FavoriteStatusResponse)
def get_status(target_type: FavoriteType, target_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    is_favorited, favorite_id = FavoriteService.get_favorite_status(db, user, target_type, target_id)
    return FavoriteStatusResponse(is_favorited=is_favorited, favorite_id=favorite_id)


@router.get("", response_model=list[FavoriteResponse])
def list_favorites(target_type: FavoriteType | None = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return FavoriteService.list_user_favorites(db, user, target_type)
