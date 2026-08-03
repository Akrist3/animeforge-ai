from sqlalchemy import Boolean, Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    projects = relationship(
    "Project",
    back_populates="owner",
    cascade="all, delete-orphan",
    )

    password_hash = Column(String(255), nullable=True)

    auth_provider = Column(String(20), default="local", nullable=False)
    google_id = Column(String(255), unique=True, nullable=True)
    profile_picture = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)