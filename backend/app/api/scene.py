from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from app.db.session import get_db

from app.models.user import User

from app.auth.oauth2 import get_current_user

from app.models.project import Project

from app.crud.project import get_project

from app.crud.scene import (
    create_scene,
    get_scenes,
    get_scene,
    update_scene,
    delete_scene,
)

from app.schemas.scene import (
    SceneCreate,
    SceneUpdate,
    SceneResponse,
)

router = APIRouter(
    prefix="/scenes",
    tags=["Scenes"],
)


@router.post(
    "/project/{project_id}",
    response_model=SceneResponse,
)
def add_scene(
    project_id: int,
    scene: SceneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_project = get_project(
        db,
        current_user.id,
        project_id,
    )

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return create_scene(
        db,
        project_id,
        scene,
    )


@router.get(
    "/project/{project_id}",
    response_model=list[SceneResponse],
)
def list_scenes(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_project = get_project(
        db,
        current_user.id,
        project_id,
    )

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return get_scenes(
        db,
        project_id,
    )


@router.put(
    "/{scene_id}",
    response_model=SceneResponse,
)
def edit_scene(
    scene_id: int,
    scene: SceneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_scene = get_scene(
        db,
        scene_id,
    )

    if not db_scene:
        raise HTTPException(
            status_code=404,
            detail="Scene not found",
        )

    return update_scene(
        db,
        db_scene,
        scene,
    )


@router.delete("/{scene_id}")
def remove_scene(
    scene_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_scene = get_scene(
        db,
        scene_id,
    )

    if not db_scene:
        raise HTTPException(
            status_code=404,
            detail="Scene not found",
        )

    delete_scene(
        db,
        db_scene,
    )

    return {
        "message": "Scene deleted successfully",
    }