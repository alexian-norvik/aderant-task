"""Tests for the RAG pipeline components."""

import pandas as pd
import pytest

import config
from src.data_loader import DataLoader
from src.executor import SafeCodeExecutor
from src.schema import generate_full_schema


class TestDataLoader:
    """Tests for DataLoader."""

    def test_load_all_returns_three_dataframes(self):
        """Test that all three Excel files are loaded."""
        loader = DataLoader(config.DATA_DIR)
        dfs = loader.load_all()

        assert "clients_df" in dfs
        assert "invoices_df" in dfs
        assert "line_items_df" in dfs

    def test_clients_has_expected_columns(self):
        """Test that clients DataFrame has expected columns."""
        loader = DataLoader(config.DATA_DIR)
        dfs = loader.load_all()

        expected_columns = ["client_id", "name", "industry", "country", "contact_email"]
        assert all(col in dfs["clients_df"].columns for col in expected_columns)

    def test_invoices_dates_are_parsed(self):
        """Test that invoice dates are parsed as datetime."""
        loader = DataLoader(config.DATA_DIR)
        dfs = loader.load_all()

        assert pd.api.types.is_datetime64_any_dtype(dfs["invoices_df"]["invoice_date"])
        assert pd.api.types.is_datetime64_any_dtype(dfs["invoices_df"]["due_date"])


class TestSchemaGeneration:
    """Tests for schema generation."""

    def test_schema_contains_all_tables(self):
        """Test that schema mentions all three tables."""
        loader = DataLoader(config.DATA_DIR)
        dfs = loader.load_all()
        schema = generate_full_schema(dfs)

        assert "clients_df" in schema
        assert "invoices_df" in schema
        assert "line_items_df" in schema

    def test_schema_contains_relationships(self):
        """Test that schema describes table relationships."""
        loader = DataLoader(config.DATA_DIR)
        dfs = loader.load_all()
        schema = generate_full_schema(dfs)

        assert "client_id" in schema
        assert "invoice_id" in schema


class TestSafeExecutor:
    """Tests for safe code execution."""

    @pytest.fixture
    def executor(self):
        """Create executor with sample data."""
        loader = DataLoader(config.DATA_DIR)
        dfs = loader.load_all()
        return SafeCodeExecutor(dfs)

    def test_simple_query_succeeds(self, executor):
        """Test that a simple pandas query works."""
        code = "result = clients_df[['name', 'country']]"
        result = executor.execute(code)

        assert result.success
        assert isinstance(result.result, pd.DataFrame)
        assert "name" in result.result.columns

    def test_missing_result_variable_fails(self, executor):
        """Test that code without 'result' variable fails."""
        code = "x = clients_df.head()"
        result = executor.execute(code)

        assert not result.success
        assert "result" in result.error.lower()

    def test_import_blocked(self, executor):
        """Test that imports are blocked."""
        code = "import os; result = os.getcwd()"
        result = executor.execute(code)

        assert not result.success
        assert "import" in result.error.lower()

    def test_exec_blocked(self, executor):
        """Test that exec/eval are blocked."""
        code = "exec('result = 1')"
        result = executor.execute(code)

        assert not result.success

    def test_aggregation_works(self, executor):
        """Test that pandas aggregations work."""
        code = "result = line_items_df.groupby('service_name').size()"
        result = executor.execute(code)

        assert result.success
        assert isinstance(result.result, pd.Series)

    def test_merge_works(self, executor):
        """Test that pandas merge/join works."""
        code = """
merged = invoices_df.merge(clients_df[['client_id', 'name']], on='client_id')
result = merged[['invoice_id', 'name']]
"""
        result = executor.execute(code)

        assert result.success
        assert isinstance(result.result, pd.DataFrame)
        assert "name" in result.result.columns
