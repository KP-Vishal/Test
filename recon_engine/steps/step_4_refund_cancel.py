"""Step 4: Refund/Cancel handling for same-day exclusion and historical adjustments."""

from __future__ import annotations

from datetime import timedelta

from recon_engine.models.adjustment import Adjustment
from recon_engine.models.error import ERROR_MESSAGES, TransactionError
from recon_engine.models.transaction import Transaction


def run(
    bijlipay_base: list[Transaction],
    existing_errors: list[TransactionError],
    payout_history: list[dict],
) -> tuple[list[Transaction], list[TransactionError], list[Adjustment]]:
    """Apply mandatory refund/cancel rules from BRD.

    1) Same-day success + refund/cancel => Error 8 and exclude from payout.
    2) If no same-day pair in current base, check previous 2-day payout history.
       - Found => generate Adjustment (hold/recover).
       - Not found => Error 9.
    """
    errors = list(existing_errors)
    adjustments: list[Adjustment] = []

    success_by_key = {
        _success_key(txn): txn
        for txn in bijlipay_base
        if txn.status == "SUCCESS" and txn.event_type == "SALE"
    }

    payout_eligible: list[Transaction] = []

    history_lookup = {
        (str(row.get("rrn", "")), row.get("tid"), row.get("order_id"), row.get("amount")): row
        for row in payout_history
    }

    for txn in bijlipay_base:
        if txn.event_type not in {"REFUND", "CANCEL"}:
            payout_eligible.append(txn)
            continue

        matching_sale = success_by_key.get(_success_key(txn))
        if matching_sale and matching_sale.txn_date == txn.txn_date:
            errors.append(_error(txn, "8"))
            continue

        key = (txn.rrn, txn.tid, txn.order_id, txn.amount)
        past = history_lookup.get(key)
        if past and _within_last_two_days(txn.recon_date, past["recon_date"]):
            adjustments.append(
                Adjustment(
                    recon_date=txn.recon_date,
                    source_file=txn.source_file,
                    rail=txn.rail,
                    rrn=txn.rrn,
                    tid=txn.tid,
                    order_id=txn.order_id,
                    txn_date=txn.txn_date,
                    original_payout_date=past["recon_date"],
                    amount=txn.amount,
                )
            )
        else:
            errors.append(_error(txn, "9"))

    return payout_eligible, errors, adjustments


def _success_key(txn: Transaction) -> tuple:
    return (txn.rail, txn.rrn, txn.tid, txn.order_id, txn.amount)


def _within_last_two_days(recon_date, prior_recon_date) -> bool:
    return recon_date - timedelta(days=2) <= prior_recon_date <= recon_date - timedelta(days=1)


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
