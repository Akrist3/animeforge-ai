from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.oauth2 import get_current_user

from app.models.user import User

from app.crud.project import get_project

from app.crud.scene import get_scene
from app.crud.generation_job import (
    create_generation_job,
    get_generation_job,
    get_scene_generation_jobs,
)

from app.schemas.generation_job import GenerationJobResponse

from app.services.generation_service import process_generation_job

router = APIRouter(
    prefix="/generation",
    tags=["Generation Jobs"],
)


@router.post(
    "/scene/{scene_id}",
    response_model=GenerationJobResponse,
)
def create_job(
    scene_id: int,
    generation_type: str,
    background_tasks: BackgroundTasks,
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

    # Check scene's project ownership
    project = get_project(
        db,
        current_user.id,
        scene.project_id,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Scene not found",
        )

    allowed_types = {
        "image",
        "video",
        "voice",
    }

    if generation_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid generation type",
        )

    job = create_generation_job(
        db,
        scene_id,
        generation_type,
    )

    background_tasks.add_task(
        process_generation_job,
        job.id,
    )

    return job
@router.get(
    "/{job_id}",
    response_model=GenerationJobResponse,
)
@router.get(
    "/{job_id}",
    response_model=GenerationJobResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_generation_job(
        db,
        job_id,
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found",
        )

    scene = get_scene(
        db,
        job.scene_id,
    )

    if not scene:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found",
        )

    project = get_project(
        db,
        current_user.id,
        scene.project_id,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found",
        )

    return job

@router.get(
    "/scene/{scene_id}",
    response_model=list[GenerationJobResponse],
)
@router.get(
    "/scene/{scene_id}",
    response_model=list[GenerationJobResponse],
)
def get_scene_jobs(
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

    project = get_project(
        db,
        current_user.id,
        scene.project_id,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Scene not found",
        )

    return get_scene_generation_jobs(
        db,
        scene_id,
    )