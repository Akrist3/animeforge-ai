from app.db.session import SessionLocal

from app.models.generation_job import GenerationJob
from app.models.scene import Scene

from app.crud.generation_job import update_generation_job

from app.providers.image_provider import generate_image


def process_generation_job(job_id: int):
    """
    Process a generation job in the background.
    """

    db = SessionLocal()

    try:
        # Get generation job
        job = (
            db.query(GenerationJob)
            .filter(GenerationJob.id == job_id)
            .first()
        )

        if not job:
            return

        # Mark job as processing
        update_generation_job(
            db,
            job,
            status="processing",
        )

        # Get scene explicitly
        scene = (
            db.query(Scene)
            .filter(Scene.id == job.scene_id)
            .first()
        )

        if not scene:
            update_generation_job(
                db,
                job,
                status="failed",
                error_message="Scene not found",
            )
            return

        # IMAGE GENERATION
        if job.generation_type == "image":

            image_url = generate_image(
                scene.prompt
            )

            # Save generated image URL
            scene.image_url = image_url

            # Mark job completed
            update_generation_job(
                db,
                job,
                status="completed",
                result_url=image_url,
            )

            return

        # VIDEO / VOICE not implemented yet
        update_generation_job(
            db,
            job,
            status="failed",
            error_message=(
                f"Generation type '{job.generation_type}' "
                "is not implemented yet"
            ),
        )

    except Exception as e:

        db.rollback()

        job = (
            db.query(GenerationJob)
            .filter(GenerationJob.id == job_id)
            .first()
        )

        if job:
            update_generation_job(
                db,
                job,
                status="failed",
                error_message=str(e),
            )

    finally:
        db.close()