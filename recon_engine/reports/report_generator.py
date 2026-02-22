"""Report generation utilities backed by DB-reproducible data."""

from __future__ import annotations

import csv
from pathlib import Path


def write_csv(path: str | Path, rows: list[dict]) -> None:
    """Write rows into a deterministic CSV report."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def generate_reports(
    bijlipay_rows: list[dict],
    payout_rows_by_rail: dict[str, list[dict]],
    adjustments_rows: list[dict],
    host_recon_errors: list[dict],
    credit_rows: list[dict],
    out_dir: str = "output",
) -> None:
    """Generate all mandatory outputs from provided table snapshots."""
    write_csv(Path(out_dir) / "bijlipay_transaction_report.csv", bijlipay_rows)

    for rail, rows in payout_rows_by_rail.items():
        write_csv(Path(out_dir) / f"payout_{rail.lower()}.csv", rows)

    write_csv(Path(out_dir) / "adjustment_report.csv", adjustments_rows)
    write_csv(Path(out_dir) / "host_reconciliation_report.csv", host_recon_errors)
    write_csv(Path(out_dir) / "credit_mismatch_report.csv", credit_rows)
