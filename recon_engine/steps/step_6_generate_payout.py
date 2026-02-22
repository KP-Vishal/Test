"""Step 6: Generate rail-wise payout table entries."""

from __future__ import annotations

from collections import defaultdict

from recon_engine.models.transaction import Transaction


def run(eligible_transactions: list[Transaction]) -> dict[str, list[dict]]:
    """Create deterministic payout output grouped by rail."""
    payouts: dict[str, list[dict]] = defaultdict(list)
    for txn in eligible_transactions:
        if txn.status != "SUCCESS" or txn.event_type != "SALE":
            continue
        payouts[txn.rail.upper()].append(
            {
                "recon_date": txn.recon_date,
                "source_file": txn.source_file,
                "rail": txn.rail,
                "rrn": txn.rrn,
                "tid": txn.tid,
                "order_id": txn.order_id,
                "txn_date": txn.txn_date,
                "amount": txn.amount,
                "payout_status": "READY",
                "created_at": txn.created_at,
            }
        )
    return dict(payouts)
