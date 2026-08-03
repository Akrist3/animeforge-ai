from sqlalchemy.orm import Session

from app.models.scene import Scene
from app.schemas.scene import SceneCreate, SceneUpdate


def create_scene(
    db: Session,
    project_id: int,
    scene: SceneCreate,
):
    db_scene = Scene(
        title=scene.title,
        prompt=scene.prompt,
        project_id=project_id,
    )

    db.add(db_scene)
    db.commit()
    db.refresh(db_scene)

    return db_scene


def get_scenes(
    db: Session,
    project_id: int,
):
    return (
        db.query(Scene)
        .filter(Scene.project_id == project_id)
        .all()
    )


def get_scene(
    db: Session,
    scene_id: int,
):
    return (
        db.query(Scene)
        .filter(Scene.id == scene_id)
        .first()
    )


def update_scene(
    db: Session,
    db_scene: Scene,
    scene: SceneUpdate,
):
    data = scene.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_scene, key, value)

    db.commit()
    db.refresh(db_scene)

    return db_scene


def delete_scene(
    db: Session,
    db_scene: Scene,
):
    db.delete(db_scene)
    db.commit()