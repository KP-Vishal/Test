"""Step 9: Bank credit validation (amount + date aggregation only)."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal


def run(payout_rows: list[dict], bank_credit_rows: list[dict]) -> list[dict]:
    """Validate credited totals by date; no transaction-level matching."""
    expected = defaultdict(lambda: Decimal("0.00"))
    credited = defaultdict(lambda: Decimal("0.00"))

    for row in payout_rows:
        expected[row["recon_date"]] += row["amount"]

    for row in bank_credit_rows:
        credited[row["credit_date"]] += row["amount"]

    results: list[dict] = []
    for credit_date in sorted(set(expected.keys()) | set(credited.keys())):
        exp = expected[credit_date]
        got = credited[credit_date]
        results.append(
            {
                "recon_date": credit_date,
                "source_file": "credit_validation",
                "rail": "ALL",
                "credit_date": credit_date,
                "expected_amount": exp,
                "credited_amount": got,
                "mismatch": exp - got,
            }
        )
    return results
