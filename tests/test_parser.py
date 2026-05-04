from tradedoc_ai.parser import extract_document_fields


def test_extracts_financial_fields():
    text = """
    Account 7890
    Transaction 2026-01-02 ACH CREDIT Payroll $2450.50
    Transaction 2026-01-03 CARD DEBIT Grocery -$82.10
    Ending balance $9368.44
    """

    result = extract_document_fields(text)

    assert result.account_id == "7890"
    assert result.ending_balance == 9368.44
    assert len(result.transactions) == 2
    assert result.transactions[0].direction == "credit"
    assert result.transactions[1].direction == "debit"

