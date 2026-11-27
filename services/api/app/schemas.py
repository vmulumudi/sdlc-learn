from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=10_000)


class NoteOut(BaseModel):
    # from_attributes: build straight from a SQLAlchemy Note object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    created_at: datetime


class SearchHit(NoteOut):
    score: float  # cosine similarity, 1.0 = identical direction
