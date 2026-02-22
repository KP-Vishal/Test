"""Step 7: Build consolidated Host transaction base with latest-status dedup."""

from __future__ import annotations

from recon_engine.models.transaction import Transaction


def run(host_transactions: list[Transaction]) -> list[Transaction]:
    """Normalize/deduplicate host transactions retaining latest status per key."""
    dedup: dict[tuple, Transaction] = {}
    for txn in sorted(host_transactions, key=lambda x: (x.host_key(), x.created_at)):
        dedup[txn.host_key()] = txn
    return list(dedup.values())
