"""Input file loader for deterministic batch ingestion."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


class FileLoader:
    """Loads CSV files without mutating originals."""

    @staticmethod
    def load_csv(path: str | Path) -> list[dict[str, str]]:
        """Return all rows from a CSV file as dictionaries."""
        with open(path, newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    @staticmethod
    def iter_csv(path: str | Path) -> Iterable[dict[str, str]]:
        """Yield rows from CSV file for memory-efficient ingestion."""
        with open(path, newline="", encoding="utf-8") as handle:
            yield from csv.DictReader(handle)
