from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache_get, cache_set
from app.config import settings
from app.db import get_session
from app.embedding import embed
from app.models import Note
from app.schemas import NoteCreate, NoteOut, SearchHit

# Everything under /api so the frontend's nginx can proxy one path prefix to this service.
router = APIRouter(prefix="/api", tags=["notes"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.post("/notes", response_model=NoteOut, status_code=201)
async def create_note(payload: NoteCreate, session: Session) -> Note:
    note = Note(
        title=payload.title,
        body=payload.body,
        embedding=embed(f"{payload.title} {payload.body}"),
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)  # load DB-generated columns (id, created_at)
    return note


@router.get("/notes", response_model=list[NoteOut])
async def list_notes(
    session: Session, limit: Annotated[int, Query(ge=1, le=100)] = 20
) -> list[Note]:
    result = await session.scalars(select(Note).order_by(Note.id.desc()).limit(limit))
    return list(result)


@router.get("/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: int, session: Session, response: Response) -> NoteOut:
    """Cache-aside read. The X-Cache header makes the cache visible from curl."""
    key = f"note:{note_id}"
    # cache_get/cache_set never raise: the cache is an optimisation, not a dependency.
    if cached := await cache_get(key):
        response.headers["X-Cache"] = "HIT"
        return NoteOut.model_validate_json(cached)

    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="note not found")
    out = NoteOut.model_validate(note)
    await cache_set(key, out.model_dump_json(), settings.cache_ttl_seconds)
    response.headers["X-Cache"] = "MISS"
    return out


@router.get("/search", response_model=list[SearchHit])
async def search(
    session: Session,
    q: Annotated[str, Query(min_length=1, max_length=500)],
    k: Annotated[int, Query(ge=1, le=20)] = 5,
) -> list[SearchHit]:
    query_vec = embed(q)
    if query_vec is None:
        return []
    # <=> is pgvector's cosine-distance operator (0 = same direction, 2 = opposite).
    distance = Note.embedding.cosine_distance(query_vec).label("distance")
    rows = await session.execute(
        select(Note, distance).where(Note.embedding.is_not(None)).order_by(distance).limit(k)
    )
    return [
        SearchHit(**NoteOut.model_validate(note).model_dump(), score=round(1 - dist, 4))
        for note, dist in rows
    ]
