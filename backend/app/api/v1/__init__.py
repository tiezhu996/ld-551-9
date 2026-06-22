from fastapi import APIRouter

from app.api.v1 import auth, courses, enrollments, favorites, instructor, lessons, orders

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/v1")
api_router.include_router(courses.router, prefix="/v1")
api_router.include_router(lessons.router, prefix="/v1")
api_router.include_router(enrollments.router, prefix="/v1")
api_router.include_router(orders.router, prefix="/v1")
api_router.include_router(instructor.router, prefix="/v1")
api_router.include_router(favorites.router, prefix="/v1")
