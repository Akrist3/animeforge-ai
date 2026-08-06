from sqlalchemy.orm import Session

from app.models.scene import Scene
from app.providers.voice_provider import generate_voice


def generate_scene_voice(
    db: Session,
    scene: Scene,
):
    """
    Generate voice narration for a scene.
    """

    voice_url = generate_voice(
        scene.prompt,
    )

    scene.voice_url = voice_url

    db.commit()
    db.refresh(scene)

    return scene