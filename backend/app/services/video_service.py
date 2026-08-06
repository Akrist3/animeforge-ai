from sqlalchemy.orm import Session

from app.models.scene import Scene
from app.providers.video_provider import generate_video


def generate_scene_video(
    db: Session,
    scene: Scene,
):
    """
    Generate a video for a scene.
    """

    video_url = generate_video(
        scene.prompt,
    )

    scene.video_url = video_url

    db.commit()
    db.refresh(scene)

    return scene