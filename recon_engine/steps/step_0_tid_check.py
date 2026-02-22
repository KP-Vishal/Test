"""Step 0: Validate TID presence by rail before base creation."""

from __future__ import annotations

from recon_engine.models.error import ERROR_MESSAGES, TransactionError
from recon_engine.models.transaction import Transaction


def run(transactions: list[Transaction], existing_errors: list[TransactionError]) -> tuple[list[Transaction], list[TransactionError]]:
    """Append Error 10 for CARD transactions missing TID or unsupported device metadata.

    This step is idempotent when called once per daily run using fresh inputs.
    """
    errors = list(existing_errors)
    for txn in transactions:
        if txn.rail.upper() == "CARD" and (not txn.tid or txn.device_type == "UNSUPPORTED"):
            errors.append(
                TransactionError(
                    recon_date=txn.recon_date,
                    source_file=txn.source_file,
                    rail=txn.rail,
                    rrn=txn.rrn,
                    tid=txn.tid,
                    order_id=txn.order_id,
                    txn_date=txn.txn_date,
                    error_code="10",
                    error_message=ERROR_MESSAGES["10"],
                )
            )
    return transactions, errors
