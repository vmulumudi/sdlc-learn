import hashlib
import math
import re

from app.models import EMBEDDING_DIM

_TOKEN = re.compile(r"[a-z0-9]+")


def embed(text: str) -> list[float] | None:
    """Deterministic stand-in for a real embedding model: no API key, no cost.

    Feature hashing: each word adds +1 or -1 to one of EMBEDDING_DIM buckets, then the
    vector is L2-normalised. Texts sharing words end up close in cosine distance, which
    is enough to exercise pgvector end to end. Swap for Azure OpenAI later without
    touching the schema (only EMBEDDING_DIM would change).

    Returns None when the text has no words: a zero vector has no direction, and
    pgvector's cosine distance on it would be NaN.
    """
    vec = [0.0] * EMBEDDING_DIM
    for token in _TOKEN.findall(text.lower()):
        h = int.from_bytes(hashlib.blake2b(token.encode(), digest_size=8).digest(), "big")
        vec[h % EMBEDDING_DIM] += 1.0 if (h >> 32) & 1 else -1.0
    norm = math.sqrt(sum(v * v for v in vec))
    return [v / norm for v in vec] if norm else None
