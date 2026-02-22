"""Example daily batch execution for Bijlipay Reconciliation Engine."""

from __future__ import annotations

from datetime import date

from recon_engine.models.error import TransactionError
from recon_engine.steps import (
    step_0_tid_check,
    step_1_build_bijlipay_base,
    step_2_dqr_consistency,
    step_3_ack_validation,
    step_4_refund_cancel,
    step_5_card_prepayout,
    step_6_generate_payout,
    step_7_build_host_base,
    step_8_host_recon,
    step_9_credit_validation,
)


def run_daily_reconciliation(
    recon_date: date,
    inbound_transactions,
    host_transactions,
    payout_history,
    wl_index,
    bank_credit_rows,
):
    """Execute Steps 0-9 in deterministic order."""
    errors: list[TransactionError] = []

    _, errors = step_0_tid_check.run(inbound_transactions, errors)
    bijli_base, errors = step_1_build_bijlipay_base.run(inbound_transactions, errors)
    errors = step_2_dqr_consistency.run(bijli_base, {}, {}, errors)
    errors = step_3_ack_validation.run(bijli_base, errors)

    payout_candidates, errors, adjustments = step_4_refund_cancel.run(
        bijli_base,
        errors,
        payout_history,
    )

    payout_candidates, errors = step_5_card_prepayout.run(
        payout_candidates,
        wl_index,
        errors,
    )

    payout_by_rail = step_6_generate_payout.run(payout_candidates)
    payout_flat = [row for rows in payout_by_rail.values() for row in rows]

    host_base = step_7_build_host_base.run(host_transactions)
    errors = step_8_host_recon.run(bijli_base, host_base, errors)
    credit_validation_rows = step_9_credit_validation.run(payout_flat, bank_credit_rows)

    return {
        "recon_date": recon_date,
        "bijlipay_base": bijli_base,
        "errors": errors,
        "adjustments": adjustments,
        "payout_by_rail": payout_by_rail,
        "host_base": host_base,
        "credit_validation": credit_validation_rows,
    }
