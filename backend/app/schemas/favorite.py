from datetime import datetime

from pydantic import BaseModel

from app.constants.enums import FavoriteType
from app.schemas.course import CourseResponse


class FavoriteCreate(BaseModel):
    target_type: FavoriteType
    target_id: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    target_type: FavoriteType
    target_id: int
    created_at: datetime
    course: CourseResponse | None = None

    model_config = {"from_attributes": True}


class FavoriteStatusResponse(BaseModel):
    is_favorited: bool
    favorite_id: int | None = None
