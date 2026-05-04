from fastapi import FastAPI

from tradedoc_ai.parser import extract_document_fields
from tradedoc_ai.rag import grounded_answer, retrieve
from tradedoc_ai.schemas import AnswerResponse, AskRequest, ExtractRequest, SourceSnippet

app = FastAPI(
    title="TradeDoc AI",
    description="Financial document extraction and retrieval API.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/extract")
def extract(request: ExtractRequest):
    return extract_document_fields(request.document_text)


@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest) -> AnswerResponse:
    chunks = retrieve(request.document_text, request.question, request.top_k)
    return AnswerResponse(
        answer=grounded_answer(request.question, chunks),
        sources=[
            SourceSnippet(rank=chunk.rank, score=chunk.score, text=chunk.text)
            for chunk in chunks
        ],
    )

