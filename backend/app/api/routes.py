from fastapi import APIRouter

from app.api.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router)

from app.api.scene import router as scene_router
router.include_router(scene_router)

@router.get("/")
def home():
    return {
        "message": "Welcome to AnimeForge AI"
    }