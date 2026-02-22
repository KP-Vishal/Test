"""Error model and constants for reconciliation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(frozen=True)
class TransactionError:
    """Immutable error event appended to transaction_errors table."""

    recon_date: date
    source_file: str
    rail: str
    rrn: str
    tid: str | None
    order_id: str | None
    txn_date: date
    error_code: str
    error_message: str
    created_at: datetime = field(default_factory=datetime.utcnow)


ERROR_MESSAGES = {
    "1": "Data duplication (exclude)",
    "2": "Aggregator mismatch",
    "3": "Institution mismatch",
    "4": "Missing in UPI settlement",
    "5": "Missing in Bijlipay base",
    "6": "Ack enabled, not received",
    "7": "Ack received, not enabled",
    "A": "Ack not applicable",
    "8": "Same-day refund / cancel",
    "9": "Refund / cancel not found",
    "10": "Unsupported device",
    "11": "Bijlipay-only (missing in WL)",
    "HR-001": "Present in Bijlipay, missing in Host",
    "HR-002": "Present in Host, missing in Bijlipay",
    "HR-003": "Status mismatch",
    "HR-004": "Amount mismatch",
    "HR-005": "Identifier mismatch",
    "HR-006": "Duplicate in Host",
    "CR-001": "Bank credit amount mismatch",
}
