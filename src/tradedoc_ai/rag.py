from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class RetrievedChunk:
    rank: int
    score: float
    text: str


def chunk_text(document_text: str, max_chars: int = 450) -> list[str]:
    lines = [line.strip() for line in document_text.splitlines() if line.strip()]
    chunks: list[str] = []
    current = ""

    for line in lines:
        candidate = f"{current}\n{line}".strip()
        if len(candidate) > max_chars and current:
            chunks.append(current)
            current = line
        else:
            current = candidate

    if current:
        chunks.append(current)
    return chunks or [document_text[:max_chars]]


def retrieve(document_text: str, question: str, top_k: int = 3) -> list[RetrievedChunk]:
    chunks = chunk_text(document_text)
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(chunks + [question])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked_indexes = scores.argsort()[::-1][:top_k]

    return [
        RetrievedChunk(rank=rank + 1, score=round(float(scores[idx]), 4), text=chunks[idx])
        for rank, idx in enumerate(ranked_indexes)
    ]


def grounded_answer(question: str, chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return "I could not find relevant source text in the document."

    best = chunks[0].text.replace("\n", " ")
    return f"Based on the most relevant document snippet, {question.strip()} -> {best}"

