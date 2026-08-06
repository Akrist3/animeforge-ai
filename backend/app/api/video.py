from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.oauth2 import get_current_user
from app.models.user import User

from app.crud.scene import get_scene
from app.services.video_service import generate_scene_video

router = APIRouter(
    prefix="/videos",
    tags=["Video Generation"],
)


@router.post("/generate/{scene_id}")
def generate_video(
    scene_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI video for a scene.
    """

    scene = get_scene(
        db,
        scene_id,
    )

    if not scene:
        raise HTTPException(
            status_code=404,
            detail="Scene not found",
        )

    scene = generate_scene_video(
        db,
        scene,
    )

    return {
        "message": "Video generated successfully",
        "video_url": scene.video_url,
    }