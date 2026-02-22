"""Step 2: DQR/SQR consistency checks against aggregator and institution references."""

from __future__ import annotations

from recon_engine.models.error import ERROR_MESSAGES, TransactionError
from recon_engine.models.transaction import Transaction


def run(
    bijlipay_base: list[Transaction],
    expected_aggregator_by_tid: dict[str, str],
    expected_institution_by_tid: dict[str, str],
    existing_errors: list[TransactionError],
) -> list[TransactionError]:
    """Append Error 2 and Error 3 on mismatch for QR rails."""
    errors = list(existing_errors)
    for txn in bijlipay_base:
        if txn.rail.upper() not in {"DQR", "SQR"}:
            continue
        if txn.tid and expected_aggregator_by_tid.get(txn.tid) not in {None, txn.aggregator_id}:
            errors.append(_error(txn, "2"))
        if txn.tid and expected_institution_by_tid.get(txn.tid) not in {None, txn.institution_id}:
            errors.append(_error(txn, "3"))
    return errors


def _error(txn: Transaction, code: str) -> TransactionError:
    return TransactionError(
        recon_date=txn.recon_date,
        source_file=txn.source_file,
        rail=txn.rail,
        rrn=txn.rrn,
        tid=txn.tid,
        order_id=txn.order_id,
        txn_date=txn.txn_date,
        error_code=code,
        error_message=ERROR_MESSAGES[code],
    )
