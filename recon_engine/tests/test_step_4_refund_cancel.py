from datetime import date
from decimal import Decimal

from recon_engine.models.transaction import Transaction
from recon_engine.steps import step_4_refund_cancel


def _txn(event_type: str, status: str = "SUCCESS") -> Transaction:
    return Transaction(
        recon_date=date(2024, 1, 3),
        source_file="day3.csv",
        rail="CARD",
        rrn="123",
        tid="T1",
        order_id=None,
        txn_date=date(2024, 1, 3),
        amount=Decimal("100.00"),
        status=status,
        event_type=event_type,
    )


def test_same_day_refund_marked_error_8_and_excluded():
    base = [_txn("SALE"), _txn("REFUND")]
    payout, errors, adjustments = step_4_refund_cancel.run(base, [], [])
    assert len(payout) == 1
    assert payout[0].event_type == "SALE"
    assert any(e.error_code == "8" for e in errors)
    assert adjustments == []


def test_missing_in_day_but_found_in_previous_payout_creates_adjustment():
    base = [_txn("REFUND")]
    payout_history = [{"rrn": "123", "tid": "T1", "order_id": None, "amount": Decimal("100.00"), "recon_date": date(2024, 1, 2)}]
    payout, errors, adjustments = step_4_refund_cancel.run(base, [], payout_history)
    assert payout == []
    assert errors == []
    assert len(adjustments) == 1
