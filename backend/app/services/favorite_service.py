from sqlalchemy.orm import Session, joinedload

from app.constants.enums import FavoriteType
from app.exceptions.course import CourseNotFoundException
from app.models.course import Course
from app.models.favorite import Favorite
from app.models.user import User
from app.services.audit_service import AuditService


class FavoriteService:
    @staticmethod
    def toggle_favorite(db: Session, user: User, target_type: FavoriteType, target_id: int, ip_address: str | None = None) -> tuple[Favorite, bool]:
        if target_type == FavoriteType.COURSE:
            course = db.get(Course, target_id)
            if not course:
                raise CourseNotFoundException("课程不存在")

        existing = db.query(Favorite).filter_by(
            user_id=user.id,
            target_type=target_type,
            target_id=target_id
        ).first()

        if existing:
            db.delete(existing)
            db.commit()
            AuditService.record(
                db,
                user_id=user.id,
                action="DELETE",
                entity="Favorite",
                entity_id=str(existing.id),
                before_data={"target_type": target_type.value, "target_id": target_id},
                ip_address=ip_address
            )
            return existing, False

        favorite = Favorite(
            user_id=user.id,
            target_type=target_type,
            target_id=target_id
        )
        db.add(favorite)
        db.flush()
        AuditService.record(
            db,
            user_id=user.id,
            action="CREATE",
            entity="Favorite",
            entity_id=str(favorite.id),
            after_data={"target_type": target_type.value, "target_id": target_id},
            ip_address=ip_address
        )
        db.commit()
        db.refresh(favorite)
        return favorite, True

    @staticmethod
    def get_favorite_status(db: Session, user: User, target_type: FavoriteType, target_id: int) -> tuple[bool, int | None]:
        existing = db.query(Favorite).filter_by(
            user_id=user.id,
            target_type=target_type,
            target_id=target_id
        ).first()
        return (True, existing.id) if existing else (False, None)

    @staticmethod
    def list_user_favorites(db: Session, user: User, target_type: FavoriteType | None = None) -> list[Favorite]:
        query = (
            db.query(Favorite)
            .filter(Favorite.user_id == user.id)
            .order_by(Favorite.created_at.desc())
        )
        if target_type:
            query = query.filter(Favorite.target_type == target_type)
        favorites = query.all()

        for fav in favorites:
            if fav.target_type == FavoriteType.COURSE:
                fav.course = (
                    db.query(Course)
                    .options(joinedload(Course.instructor))
                    .filter(Course.id == fav.target_id)
                    .first()
                )
        return favorites
