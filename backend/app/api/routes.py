from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.scene import router as scene_router
from app.api.image import router as image_router
from app.api.video import router as video_router
from app.api.voice import router as voice_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(scene_router)
router.include_router(image_router)
router.include_router(video_router)
router.include_router(voice_router)


@router.get("/")
def home():
    return {
        "message": "Welcome to AnimeForge AI"
    }