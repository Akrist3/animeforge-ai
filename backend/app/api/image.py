from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.oauth2 import get_current_user
from app.models.user import User

from app.crud.scene import get_scene
from app.services.image_service import generate_scene_image

router = APIRouter(
    prefix="/images",
    tags=["Image Generation"],
)


@router.post("/generate/{scene_id}")
def generate_image(
    scene_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an AI image for a scene.
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

    scene = generate_scene_image(
        db,
        scene,
    )

    return {
        "message": "Image generated successfully",
        "image_url": scene.image_url,
    }

@router.post("/generate/{scene_id}")
def generate_image(
    scene_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print("Received Scene ID:", scene_id)

    scene = get_scene(
        db,
        scene_id,
    )

    print("Scene Found:", scene)

    if not scene:
        raise HTTPException(
            status_code=404,
            detail="Scene not found",
        )

    scene = generate_scene_image(
        db,
        scene,
    )

    return {
        "message": "Image generated successfully",
        "image_url": scene.image_url,
    }