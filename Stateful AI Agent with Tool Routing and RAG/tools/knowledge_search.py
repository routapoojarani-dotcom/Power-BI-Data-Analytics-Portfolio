"""A local knowledge tool with lexical retrieval and an optional FAISS backend."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Any

from langchain_core.tools import tool

from src.config import PROJECT_ROOT, get_settings

KNOWLEDGE_DIR = PROJECT_ROOT / "data" / "knowledge"
_WORD = re.compile(r"[a-zA-Z0-9]+")


def _tokens(text: str) -> set[str]:
    return {word.lower() for word in _WORD.findall(text) if len(word) > 2}


@lru_cache(maxsize=1)
def _paragraphs() -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        for index, paragraph in enumerate(re.split(r"\n\s*\n", path.read_text(encoding="utf-8"))):
            cleaned = paragraph.strip()
            if cleaned:
                chunks.append(
                    {"source": path.name, "chunk": str(index + 1), "content": cleaned}
                )
    return chunks


def lexical_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    query_tokens = _tokens(query)
    if not query_tokens:
        return []
    ranked: list[tuple[float, dict[str, str]]] = []
    for chunk in _paragraphs():
        chunk_tokens = _tokens(chunk["content"])
        overlap = query_tokens & chunk_tokens
        score = len(overlap) / max(len(query_tokens), 1)
        if score:
            ranked.append((score, chunk))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [
        {**chunk, "score": round(score, 3), "retriever": "lexical"}
        for score, chunk in ranked[:top_k]
    ]


@lru_cache(maxsize=1)
def _faiss_store() -> Any:
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as exc:
        raise RuntimeError(
            "FAISS mode requires: pip install -r requirements-rag.txt"
        ) from exc

    settings = get_settings()
    chunks = _paragraphs()
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model_name)
    return FAISS.from_texts(
        [chunk["content"] for chunk in chunks],
        embeddings,
        metadatas=[{"source": chunk["source"], "chunk": chunk["chunk"]} for chunk in chunks],
    )


def faiss_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    documents = _faiss_store().similarity_search_with_score(query, k=top_k)
    return [
        {
            "source": document.metadata.get("source", "unknown"),
            "chunk": str(document.metadata.get("chunk", "")),
            "content": document.page_content,
            "distance": round(float(distance), 3),
            "retriever": "faiss",
        }
        for document, distance in documents
    ]


def search_documents(query: str, top_k: int | None = None) -> dict[str, Any]:
    if not isinstance(query, str) or not query.strip():
        return {"found": False, "error": "query is required", "results": []}
    settings = get_settings()
    selected_top_k = top_k or settings.rag_top_k
    results = (
        faiss_search(query, selected_top_k)
        if settings.use_faiss_rag
        else lexical_search(query, selected_top_k)
    )
    return {"found": bool(results), "query": query, "results": results}


@tool("knowledge_search")
def knowledge_search(query: str) -> str:
    """Search local company-policy documents and return grounded excerpts with source names."""

    return json.dumps(search_documents(query), ensure_ascii=False)

