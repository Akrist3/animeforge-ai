from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)

    scene_id = Column(
        Integer,
        ForeignKey("scenes.id", ondelete="CASCADE"),
        nullable=False,
    )

    generation_type = Column(
        String(20),
        nullable=False,
    )

    status = Column(
        String(20),
        default="pending",
        nullable=False,
    )

    result_url = Column(
        Text,
        nullable=True,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    scene = relationship(
        "Scene",
        back_populates="generation_jobs",
    )