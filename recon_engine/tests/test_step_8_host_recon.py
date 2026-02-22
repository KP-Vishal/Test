from datetime import date
from decimal import Decimal

from recon_engine.models.transaction import Transaction
from recon_engine.steps import step_8_host_recon


def _txn(source: str, status: str = "SUCCESS", amount: str = "100.00") -> Transaction:
    return Transaction(
        recon_date=date(2024, 1, 3),
        source_file=source,
        rail="CARD",
        rrn="123",
        tid="T1",
        order_id=None,
        txn_date=date(2024, 1, 3),
        amount=Decimal(amount),
        status=status,
        event_type="SALE",
    )


def test_hr001_when_missing_in_host():
    errors = step_8_host_recon.run([_txn("bijli.csv")], [], [])
    assert any(e.error_code == "HR-001" for e in errors)


def test_hr003_and_hr004_for_status_and_amount_mismatch():
    bijli = [_txn("bijli.csv", status="SUCCESS", amount="100.00")]
    host = [_txn("host.csv", status="FAILURE", amount="200.00")]
    errors = step_8_host_recon.run(bijli, host, [])
    assert any(e.error_code == "HR-003" for e in errors)
    assert any(e.error_code == "HR-004" for e in errors)
