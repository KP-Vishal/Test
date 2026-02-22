"""Step 5: Card pre-payout validation producing Error 11 as needed."""

from __future__ import annotations

from recon_engine.models.error import ERROR_MESSAGES, TransactionError
from recon_engine.models.transaction import Transaction


def run(
    payout_candidates: list[Transaction],
    wl_index: set[tuple],
    existing_errors: list[TransactionError],
) -> tuple[list[Transaction], list[TransactionError]]:
    """Exclude CARD rows not present in WL source and mark Error 11."""
    errors = list(existing_errors)
    eligible: list[Transaction] = []

    for txn in payout_candidates:
        if txn.rail.upper() != "CARD":
            eligible.append(txn)
            continue

        key = (txn.rrn, txn.tid, txn.amount)
        if key not in wl_index:
            errors.append(
                TransactionError(
                    recon_date=txn.recon_date,
                    source_file=txn.source_file,
                    rail=txn.rail,
                    rrn=txn.rrn,
                    tid=txn.tid,
                    order_id=txn.order_id,
                    txn_date=txn.txn_date,
                    error_code="11",
                    error_message=ERROR_MESSAGES["11"],
                )
            )
            continue

        eligible.append(txn)

    return eligible, errors
