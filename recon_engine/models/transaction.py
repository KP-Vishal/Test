"""Transaction model used throughout the reconciliation pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any


@dataclass(frozen=False)
class Transaction:
    """Canonical transaction representation.

    A transaction is mutable only for status/error enrichment during deterministic
    step execution. Monetary and identifier fields are never auto-corrected.
    """

    recon_date: date
    source_file: str
    rail: str
    rrn: str
    tid: str | None
    order_id: str | None
    txn_date: date
    amount: Decimal
    status: str
    event_type: str
    aggregator_id: str | None = None
    institution_id: str | None = None
    ack_enabled: bool | None = None
    ack_received: bool | None = None
    device_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def natural_key(self) -> tuple:
        """Return deterministic key by rail based on BRD matching rules."""
        if self.rail.upper() == "CARD":
            return (self.rail, self.rrn, self.tid, self.amount)

        if self.rail.upper() in {"DQR", "SQR"}:
            if self.order_id:
                return (self.rail, self.rrn, self.amount, self.order_id)
            return (self.rail, self.rrn, self.amount, self.txn_date)

        return (self.rail, self.rrn, self.amount, self.txn_date)

    def host_key(self) -> tuple:
        """Alias used for host dedup and recon matching."""
        return self.natural_key()
