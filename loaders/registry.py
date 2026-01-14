# loaders/registry.py
import csv
from pathlib import Path
from typing import Dict, Any, List

class DatasetRegistry:
    def __init__(self, csv_path: str = "metadata_clean.csv"):
        self.csv_path = Path(csv_path)
        self._rows: List[Dict[str, Any]] = []
        self._by_index: Dict[str, Dict[str, Any]] = {}
        self._by_name: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(self.csv_path)
        with self.csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self._rows = rows
        for row in rows:
            idx = str(row.get("INDEX", "")).strip()
            name = str(row.get("NAME", "")).strip()
            if idx:
                self._by_index[idx] = row
            if name:
                self._by_name[name.lower()] = row

    def list_all(self) -> List[Dict[str, Any]]:
        return self._rows

    def get(self, index: int | str) -> Dict[str, Any]:
        index = str(index)
        if index not in self._by_index:
            raise KeyError(f"No dataset with INDEX={index}")
        return self._by_index[index]

    def get_by_name(self, name: str) -> Dict[str, Any]:
        key = name.lower()
        if key not in self._by_name:
            raise KeyError(f"No dataset with NAME='{name}'")
        return self._by_name[key]

    def link(self, index: int | str) -> str:
        row = self.get(index)
        url = (row.get("MAIN_LINK") or "").strip()
        if not url:
            raise KeyError(f"No MAIN_LINK for INDEX={index}")
        return url

    def pretty(self, index: int | str) -> str:
        row = self.get(index)
        return f"[{row['INDEX']}] {row['NAME']} ({row['CATEGORY']}, {row['SIZE']})"
