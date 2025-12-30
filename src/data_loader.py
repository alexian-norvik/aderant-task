"""Load Excel data files into pandas DataFrames."""

from pathlib import Path

import pandas as pd


class DataLoader:
    """Load and manage Excel data files."""

    def __init__(self, data_dir: Path | str):
        self.data_dir = Path(data_dir)
        self._dataframes: dict[str, pd.DataFrame] = {}

    def load_all(self) -> dict[str, pd.DataFrame]:
        """Load all Excel files from the data directory."""
        self._dataframes = {
            "clients_df": self._load_clients(),
            "invoices_df": self._load_invoices(),
            "line_items_df": self._load_line_items(),
        }
        return self._dataframes

    def _load_clients(self) -> pd.DataFrame:
        """Load clients data."""
        path = self.data_dir / "Clients.xlsx"
        return pd.read_excel(path)

    def _load_invoices(self) -> pd.DataFrame:
        """Load invoices data with proper date parsing."""
        path = self.data_dir / "Invoices.xlsx"
        df = pd.read_excel(path, parse_dates=["invoice_date", "due_date"])
        return df

    def _load_line_items(self) -> pd.DataFrame:
        """Load invoice line items data."""
        path = self.data_dir / "InvoiceLineItems.xlsx"
        return pd.read_excel(path)

    @property
    def dataframes(self) -> dict[str, pd.DataFrame]:
        """Get loaded dataframes."""
        if not self._dataframes:
            self.load_all()
        return self._dataframes
