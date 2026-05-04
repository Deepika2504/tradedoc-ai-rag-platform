from pydantic import BaseModel, Field


class Transaction(BaseModel):
    date: str = Field(description="ISO-like transaction date found in the document")
    description: str
    amount: float
    direction: str = Field(description="credit, debit, or unknown")


class DocumentExtraction(BaseModel):
    account_id: str | None
    ending_balance: float | None
    transactions: list[Transaction]
    warnings: list[str] = []


class ExtractRequest(BaseModel):
    document_text: str


class AskRequest(BaseModel):
    document_text: str
    question: str
    top_k: int = 3


class SourceSnippet(BaseModel):
    rank: int
    score: float
    text: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceSnippet]

