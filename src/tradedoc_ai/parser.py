import re

from tradedoc_ai.schemas import DocumentExtraction, Transaction


ACCOUNT_RE = re.compile(r"\baccount(?:\s+number)?\s*[:#]?\s*(?P<account>[A-Za-z0-9-]{4,})", re.I)
BALANCE_RE = re.compile(r"\bending\s+balance\s*[:$]?\s*\$?(?P<balance>-?[\d,]+(?:\.\d{2})?)", re.I)
TRANSACTION_RE = re.compile(
    r"\btransaction\s+"
    r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<description>.*?)\s+"
    r"(?P<amount>-?\$?-?[\d,]+(?:\.\d{2})?)\b",
    re.I,
)


def _to_float(value: str) -> float:
    normalized = value.replace(",", "").replace("$", "")
    if normalized.count("-") > 1:
        normalized = "-" + normalized.replace("-", "")
    return float(normalized)


def extract_document_fields(document_text: str) -> DocumentExtraction:
    account_match = ACCOUNT_RE.search(document_text)
    balance_match = BALANCE_RE.search(document_text)
    transactions: list[Transaction] = []

    for match in TRANSACTION_RE.finditer(document_text):
        amount = _to_float(match.group("amount"))
        description = " ".join(match.group("description").split())
        direction = "credit" if amount > 0 else "debit" if amount < 0 else "unknown"
        transactions.append(
            Transaction(
                date=match.group("date"),
                description=description,
                amount=amount,
                direction=direction,
            )
        )

    warnings = []
    if not transactions:
        warnings.append("No transaction rows matched the expected pattern.")
    if not balance_match:
        warnings.append("Ending balance was not detected.")

    return DocumentExtraction(
        account_id=account_match.group("account") if account_match else None,
        ending_balance=_to_float(balance_match.group("balance")) if balance_match else None,
        transactions=transactions,
        warnings=warnings,
    )
