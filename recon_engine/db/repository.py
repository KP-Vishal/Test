"""Database repository abstraction for idempotent writes and reads."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Iterable, Sequence

import psycopg
from psycopg.rows import dict_row

from recon_engine.models.adjustment import Adjustment
from recon_engine.models.error import TransactionError
from recon_engine.models.transaction import Transaction


class Repository:
    """Thin PostgreSQL repository with explicit, deterministic operations."""

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def _connect(self) -> psycopg.Connection:
        return psycopg.connect(self.dsn, row_factory=dict_row)

    def execute_schema(self, schema_sql: str) -> None:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(schema_sql)
            conn.commit()

    def insert_bijlipay_base(self, rows: Iterable[Transaction]) -> None:
        query = """
        INSERT INTO bijlipay_transaction_base (
            recon_date, source_file, rail, rrn, tid, order_id, txn_date, amount,
            status, event_type, aggregator_id, institution_id, ack_enabled,
            ack_received, device_type, metadata, created_at
        ) VALUES (
            %(recon_date)s, %(source_file)s, %(rail)s, %(rrn)s, %(tid)s,
            %(order_id)s, %(txn_date)s, %(amount)s, %(status)s, %(event_type)s,
            %(aggregator_id)s, %(institution_id)s, %(ack_enabled)s,
            %(ack_received)s, %(device_type)s, %(metadata)s, %(created_at)s
        )
        """
        payload = [asdict(r) for r in rows]
        if not payload:
            return
        with self._connect() as conn, conn.cursor() as cur:
            cur.executemany(query, payload)
            conn.commit()

    def insert_errors(self, errors: Iterable[TransactionError]) -> None:
        query = """
        INSERT INTO transaction_errors (
            recon_date, source_file, rail, rrn, tid, order_id, txn_date,
            error_code, error_message, created_at
        ) VALUES (
            %(recon_date)s, %(source_file)s, %(rail)s, %(rrn)s, %(tid)s,
            %(order_id)s, %(txn_date)s, %(error_code)s, %(error_message)s,
            %(created_at)s
        )
        """
        payload = [asdict(e) for e in errors]
        if not payload:
            return
        with self._connect() as conn, conn.cursor() as cur:
            cur.executemany(query, payload)
            conn.commit()

    def insert_adjustments(self, rows: Iterable[Adjustment]) -> None:
        query = """
        INSERT INTO adjustments (
            recon_date, source_file, rail, rrn, tid, order_id, txn_date,
            original_payout_date, amount, adjustment_type, created_at
        ) VALUES (
            %(recon_date)s, %(source_file)s, %(rail)s, %(rrn)s, %(tid)s,
            %(order_id)s, %(txn_date)s, %(original_payout_date)s, %(amount)s,
            %(adjustment_type)s, %(created_at)s
        )
        """
        payload = [asdict(r) for r in rows]
        if not payload:
            return
        with self._connect() as conn, conn.cursor() as cur:
            cur.executemany(query, payload)
            conn.commit()

    def find_payout_history(self, keys: Sequence[tuple], from_date: date, to_date: date) -> list[dict]:
        if not keys:
            return []
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM payouts
                WHERE recon_date BETWEEN %s AND %s
                  AND (rrn, COALESCE(tid, ''), COALESCE(order_id, ''), amount)
                      = ANY(%s)
                """,
                (from_date, to_date, list(keys)),
            )
            return cur.fetchall()
