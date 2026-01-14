# loaders/registry.py
import csv
from pathlib import Path
from typing import Dict, Any, List, Union, Optional

class DatasetRegistry:
    def __init__(self, csv_path: str = r"F:\ML\Adverse-Weather-and-Low-Light-Vision-Datasets\datasets\datasets.csv"):
        self.csv_path = Path(csv_path)
        self._rows: List[Dict[str, Any]] = []
        self._by_index: Dict[str, Dict[str, Any]] = {}
        self._by_name: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        """Loads and cleans data from the CSV file."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Registry file not found at: {self.csv_path}")
            
        with self.csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Remove whitespace from headers to prevent key errors
            reader.fieldnames = [field.strip() for field in reader.fieldnames] if reader.fieldnames else []
            
            for row in reader:
                # Clean up whitespace from values
                clean_row = {k: (v.strip() if v else "") for k, v in row.items()}
                
                idx = clean_row.get("INDEX", "")
                name = clean_row.get("NAME", "")
                
                if idx:
                    self._rows.append(clean_row)
                    self._by_index[idx] = clean_row
                if name:
                    self._by_name[name.lower()] = clean_row

    def list_all(self) -> List[Dict[str, Any]]:
        """Returns all datasets in the registry."""
        return self._rows

    def get(self, index: Union[int, str]) -> Dict[str, Any]:
        """Retrieves a dataset by its INDEX. Fixed for Python < 3.10."""
        idx_str = str(index).strip()
        if idx_str not in self._by_index:
            raise KeyError(f"No dataset found with INDEX='{idx_str}'")
        return self._by_index[idx_str]

    def get_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieves a dataset by its NAME (case-insensitive)."""
        key = name.strip().lower()
        if key not in self._by_name:
            raise KeyError(f"No dataset found with NAME='{name}'")
        return self._by_name[key]

    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for datasets where the query appears in Name, Category, or Description.
        """
        q = query.strip().lower()
        results = []
        for row in self._rows:
            if (q in row.get("NAME", "").lower() or 
                q in row.get("CATEGORY", "").lower() or 
                q in row.get("DESCRIPTION", "").lower()):
                results.append(row)
        return results

    def link(self, index: Union[int, str]) -> str:
        """Returns the MAIN_LINK for a specific dataset index."""
        row = self.get(index)
        url = row.get("MAIN_LINK", "").strip()
        if not url:
            raise KeyError(f"No MAIN_LINK available for INDEX={index}")
        return url

    def pretty(self, index: Union[int, str]) -> str:
        """Returns a human-readable summary string for a dataset."""
        row = self.get(index)
        return f"[{row.get('INDEX')}] {row.get('NAME')} | {row.get('CATEGORY')} | Size: {row.get('SIZE')}"

# Example usage block for testing
if __name__ == "__main__":
    try:
        reg = DatasetRegistry()
        print(f"Successfully loaded {len(reg.list_all())} datasets.")
        
        # Test Search
        results = reg.search("low light") # Search for datasets related to "low light", changing the query as needed
        print(f"\nFound {len(results)} datasets related to 'low light':")
        for res in results: # Show all found dataset names
            print(f" - {res['NAME']}")
            
    except Exception as e:
        print(f"Error: {e}")