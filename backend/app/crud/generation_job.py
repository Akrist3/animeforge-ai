from sqlalchemy.orm import Session

from app.models.generation_job import GenerationJob


def create_generation_job(
    db: Session,
    scene_id: int,
    generation_type: str,
):
    job = GenerationJob(
        scene_id=scene_id,
        generation_type=generation_type,
        status="pending",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_generation_job(
    db: Session,
    job_id: int,
):
    return (
        db.query(GenerationJob)
        .filter(GenerationJob.id == job_id)
        .first()
    )


def get_scene_generation_jobs(
    db: Session,
    scene_id: int,
):
    return (
        db.query(GenerationJob)
        .filter(GenerationJob.scene_id == scene_id)
        .order_by(GenerationJob.id.desc())
        .all()
    )


def update_generation_job(
    db: Session,
    job: GenerationJob,
    status: str,
    result_url: str | None = None,
    error_message: str | None = None,
):
    job.status = status

    if result_url is not None:
        job.result_url = result_url

    if error_message is not None:
        job.error_message = error_message

    db.commit()
    db.refresh(job)

    return job