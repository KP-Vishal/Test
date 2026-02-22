"""Step 1: Build deterministic Bijlipay transaction base with dedup error tagging."""

from __future__ import annotations

from collections import defaultdict

from recon_engine.models.error import ERROR_MESSAGES, TransactionError
from recon_engine.models.transaction import Transaction



def run(
    candidate_transactions: list[Transaction],
    existing_errors: list[TransactionError],
) -> tuple[list[Transaction], list[TransactionError]]:
    """Create Bijlipay base and append Error 1 for duplicates.

    Duplicate logic follows rail-specific natural keys.
    First-seen transaction is retained; later duplicates are excluded from output base.
    """
    grouped: dict[tuple, list[Transaction]] = defaultdict(list)
    for txn in candidate_transactions:
        grouped[txn.natural_key()].append(txn)

    base_rows: list[Transaction] = []
    errors = list(existing_errors)
    for txns in grouped.values():
        base_rows.append(txns[0])
        for duplicate in txns[1:]:
            errors.append(
                TransactionError(
                    recon_date=duplicate.recon_date,
                    source_file=duplicate.source_file,
                    rail=duplicate.rail,
                    rrn=duplicate.rrn,
                    tid=duplicate.tid,
                    order_id=duplicate.order_id,
                    txn_date=duplicate.txn_date,
                    error_code="1",
                    error_message=ERROR_MESSAGES["1"],
                )
            )

    return base_rows, errors
