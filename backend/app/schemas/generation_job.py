from pydantic import BaseModel


class GenerationJobResponse(BaseModel):
    id: int
    scene_id: int
    generation_type: str
    status: str
    result_url: str | None = None
    error_message: str | None = None

    class Config:
        from_attributes = True