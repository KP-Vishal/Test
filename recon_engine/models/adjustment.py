"""Adjustment model for hold/recovery transactions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal


@dataclass(frozen=True)
class Adjustment:
    """Represents Adju generated when refund/cancel references past payout."""

    recon_date: date
    source_file: str
    rail: str
    rrn: str
    tid: str | None
    order_id: str | None
    txn_date: date
    original_payout_date: date
    amount: Decimal
    adjustment_type: str = "HOLD_RECOVER"
    created_at: datetime = field(default_factory=datetime.utcnow)
