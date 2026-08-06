from sqlalchemy.orm import Session

from app.models.scene import Scene

from app.providers.image_provider import generate_image


def generate_scene_image(
    db: Session,
    scene: Scene,
):
    """
    Generate an image for a scene.
    """

    image_url = generate_image(
        scene.prompt,
    )

    scene.image_url = image_url

    db.commit()
    db.refresh(scene)

    return scene
    