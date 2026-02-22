"""Step 3: ACK validation step appending Error 6/7/A."""

from __future__ import annotations

from recon_engine.models.error import ERROR_MESSAGES, TransactionError
from recon_engine.models.transaction import Transaction


def run(bijlipay_base: list[Transaction], existing_errors: list[TransactionError]) -> list[TransactionError]:
    """Validate acknowledgement policy without altering transactions."""
    errors = list(existing_errors)
    for txn in bijlipay_base:
        if txn.rail.upper() == "CARD":
            errors.append(_error(txn, "A"))
            continue
        if txn.ack_enabled is True and txn.ack_received is not True:
            errors.append(_error(txn, "6"))
        elif txn.ack_enabled is False and txn.ack_received is True:
            errors.append(_error(txn, "7"))
        elif txn.ack_enabled is None:
            errors.append(_error(txn, "A"))
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
