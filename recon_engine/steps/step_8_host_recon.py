"""Step 8: Full Bijlipay vs Host reconciliation using HR error taxonomy."""

from __future__ import annotations

from collections import Counter

from recon_engine.models.error import ERROR_MESSAGES, TransactionError
from recon_engine.models.transaction import Transaction


def run(
    bijlipay_base: list[Transaction],
    host_base: list[Transaction],
    existing_errors: list[TransactionError],
) -> list[TransactionError]:
    """Compare entire bases and append host-recon errors without payout impact."""
    errors = list(existing_errors)

    host_counts = Counter(txn.host_key() for txn in host_base)
    for txn in host_base:
        if host_counts[txn.host_key()] > 1:
            errors.append(_error(txn, "HR-006"))

    host_by_identifier = {_identifier_key(txn): txn for txn in host_base}
    bijli_by_identifier = {_identifier_key(txn): txn for txn in bijlipay_base}

    for btxn in bijlipay_base:
        id_key = _identifier_key(btxn)
        htxn = host_by_identifier.get(id_key)
        if not htxn:
            errors.append(_error(btxn, "HR-001"))
            continue

        if btxn.amount != htxn.amount:
            errors.append(_error(btxn, "HR-004"))
        if btxn.status != htxn.status:
            errors.append(_error(btxn, "HR-003"))
        if btxn.natural_key() != htxn.host_key():
            errors.append(_error(btxn, "HR-005"))

    for htxn in host_base:
        if _identifier_key(htxn) not in bijli_by_identifier:
            errors.append(_error(htxn, "HR-002"))

    return errors


def _identifier_key(txn: Transaction) -> tuple:
    return (txn.rail, txn.rrn, txn.tid, txn.order_id, txn.txn_date)


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
