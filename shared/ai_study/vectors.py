"""Qdrant helper. Day 6부터 사용.

from ai_study.vectors import ensure_collection, upsert_texts, search
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from ai_study.config import settings


def client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)


def ensure_collection(
    name: str,
    *,
    dim: int = 1536,
    distance: qm.Distance = qm.Distance.COSINE,
    recreate: bool = False,
) -> QdrantClient:
    c = client()
    exists = c.collection_exists(name)
    if exists and recreate:
        c.delete_collection(name)
        exists = False
    if not exists:
        c.create_collection(
            collection_name=name,
            vectors_config=qm.VectorParams(size=dim, distance=distance),
        )
    return c


def _deterministic_id(text: str) -> str:
    return str(uuid.UUID(hashlib.md5(text.encode("utf-8")).hexdigest()))


@dataclass
class UpsertItem:
    text: str
    vector: list[float]
    payload: dict


def upsert_texts(collection: str, items: list[UpsertItem]) -> int:
    c = client()
    points = [
        qm.PointStruct(
            id=_deterministic_id(item.text),
            vector=item.vector,
            payload={"text": item.text, **item.payload},
        )
        for item in items
    ]
    c.upsert(collection_name=collection, points=points, wait=True)
    return len(points)


def search(
    collection: str,
    query_vector: list[float],
    *,
    top_k: int = 5,
    payload_filter: qm.Filter | None = None,
) -> list[qm.ScoredPoint]:
    return client().search(
        collection_name=collection,
        query_vector=query_vector,
        limit=top_k,
        query_filter=payload_filter,
    )
