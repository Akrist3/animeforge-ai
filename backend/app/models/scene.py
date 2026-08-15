from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    prompt = Column(Text, nullable=False)

    image_url = Column(Text, nullable=True)

    video_url = Column(Text, nullable=True)

    voice_url = Column(Text, nullable=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    project = relationship(
        "Project",
        back_populates="scenes",
    )
    generation_jobs = relationship(
    "GenerationJob",
    back_populates="scene",
    cascade="all, delete-orphan",
)
