from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.oauth2 import get_current_user
from app.models.user import User

from app.crud.scene import get_scene
from app.services.voice_service import generate_scene_voice

router = APIRouter(
    prefix="/voices",
    tags=["Voice Generation"],
)


@router.post("/generate/{scene_id}")
def generate_voice(
    scene_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scene = get_scene(
        db,
        scene_id,
    )

    if not scene:
        raise HTTPException(
            status_code=404,
            detail="Scene not found",
        )

    scene = generate_scene_voice(
        db,
        scene,
    )

    return {
        "message": "Voice generated successfully",
        "voice_url": scene.voice_url,
    }