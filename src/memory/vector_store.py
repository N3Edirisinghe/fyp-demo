"""
Semantic memory retrieval using ChromaDB (Section 5.2).

Stores a sentence-transformer embedding of each interaction so that
Session 2 (memory-enabled condition) can retrieve relevant past
conversations for a given participant, without simply replaying raw logs.
"""

import uuid

import chromadb
from chromadb.utils import embedding_functions

from config.settings import settings

_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def _get_client():
    """
    Returns a Chroma client. Uses Chroma Cloud in production; falls back to
    a local persistent client for development (see docs/deployment_guide.md).
    """
    if settings.chroma_api_key:
        return chromadb.CloudClient(
            api_key=settings.chroma_api_key,
            tenant=settings.chroma_tenant,
            database=settings.chroma_database,
        )
    return chromadb.PersistentClient(path=settings.local_chroma_path)


def _get_collection():
    client = _get_client()
    return client.get_or_create_collection(
        name="emotional_memory", embedding_function=_embedding_fn
    )


def store_memory(participant_id: str, session: int, text: str, emotion_label: str) -> str:
    """Embeds and stores one interaction. Returns the generated embedding id."""
    collection = _get_collection()
    embedding_id = str(uuid.uuid4())
    collection.add(
        ids=[embedding_id],
        documents=[text],
        metadatas=[
            {"participant_id": participant_id, "session": session, "emotion": emotion_label}
        ],
    )
    return embedding_id


def retrieve_relevant_memories(participant_id: str, query_text: str, top_k: int = 3) -> list[dict]:
    """
    Retrieves the top-k most semantically relevant past interactions for a
    given participant, scoped so one participant's data never leaks into
    another's session (important for both validity and ethics).
    """
    collection = _get_collection()
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        where={"participant_id": participant_id},
    )

    memories = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    for doc, meta in zip(documents, metadatas, strict=False):
        memories.append(
            {"text": doc, "emotion": meta.get("emotion"), "session": meta.get("session")}
        )
    return memories
