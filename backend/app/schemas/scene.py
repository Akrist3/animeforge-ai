from pydantic import BaseModel


class SceneBase(BaseModel):
    title: str
    prompt: str


class SceneCreate(SceneBase):
    pass


class SceneUpdate(BaseModel):
    title: str | None = None
    prompt: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    voice_url: str | None = None


class SceneResponse(SceneBase):
    id: int
    image_url: str | None = None
    video_url: str | None = None
    voice_url: str | None = None
    project_id: int

    class Config:
        from_attributes = True