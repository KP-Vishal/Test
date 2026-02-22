"""Schema normalizer converting raw rows into canonical Transaction objects."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from recon_engine.models.transaction import Transaction


class SchemaNormalizer:
    """Normalizes source-specific field names into canonical schema."""

    @staticmethod
    def normalize(row: dict, recon_date: date, source_file: str, rail: str) -> Transaction:
        """Map raw row to Transaction with deterministic defaults."""
        return Transaction(
            recon_date=recon_date,
            source_file=source_file,
            rail=rail,
            rrn=str(row.get("RRN", "")).strip(),
            tid=str(row.get("TID", "")).strip() or None,
            order_id=str(row.get("ORDER_ID", "")).strip() or None,
            txn_date=date.fromisoformat(str(row["TXN_DATE"])),
            amount=Decimal(str(row["AMOUNT"])),
            status=str(row.get("STATUS", "")).strip().upper(),
            event_type=str(row.get("EVENT_TYPE", "SALE")).strip().upper(),
            aggregator_id=str(row.get("AGGREGATOR_ID", "")).strip() or None,
            institution_id=str(row.get("INSTITUTION_ID", "")).strip() or None,
            ack_enabled=_to_bool(row.get("ACK_ENABLED")),
            ack_received=_to_bool(row.get("ACK_RECEIVED")),
            device_type=str(row.get("DEVICE_TYPE", "")).strip().upper() or None,
            metadata={k: v for k, v in row.items()},
        )


def _to_bool(value: object) -> bool | None:
    if value is None or value == "":
        return None
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "y", "yes"}:
        return True
    if normalized in {"false", "0", "n", "no"}:
        return False
    return None
