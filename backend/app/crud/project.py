from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, owner_id: int, project: ProjectCreate):
    db_project = Project(
        title=project.title,
        description=project.description,
        owner_id=owner_id,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, owner_id: int):
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .all()
    )


def get_project(db: Session, owner_id: int, project_id: int):
    return (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == owner_id,
        )
        .first()
    )


def update_project(
    db: Session,
    db_project: Project,
    project: ProjectUpdate,
):
    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, db_project: Project):
    db.delete(db_project)
    db.commit()