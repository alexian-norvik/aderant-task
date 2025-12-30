"""Generate schema descriptions for LLM context."""

import pandas as pd


def get_dtype_description(dtype) -> str:
    """Convert pandas dtype to human-readable description."""
    dtype_str = str(dtype)
    if "int" in dtype_str:
        return "integer"
    elif "float" in dtype_str:
        return "float"
    elif "datetime" in dtype_str:
        return "datetime"
    elif "object" in dtype_str:
        return "string"
    elif "bool" in dtype_str:
        return "boolean"
    return dtype_str


def generate_table_schema(df: pd.DataFrame, table_name: str) -> str:
    """Generate a schema description for a DataFrame."""
    lines = [f"### {table_name}"]
    lines.append("Columns:")

    for col in df.columns:
        dtype = get_dtype_description(df[col].dtype)
        sample_values = df[col].dropna().head(3).tolist()
        sample_str = ", ".join(str(v) for v in sample_values)
        lines.append(f"  - {col} ({dtype}): e.g., {sample_str}")

    lines.append(f"Total rows: {len(df)}")
    return "\n".join(lines)


def generate_full_schema(dataframes: dict[str, pd.DataFrame]) -> str:
    """Generate complete schema description for all tables."""
    schema_parts = [
        "# Database Schema\n",
        "You have access to the following pandas DataFrames:\n",
    ]

    table_descriptions = {
        "clients_df": "Client information",
        "invoices_df": "Invoice records with dates and status",
        "line_items_df": "Individual line items for each invoice",
    }

    for df_name, df in dataframes.items():
        desc = table_descriptions.get(df_name, "")
        schema_parts.append(f"\n## {df_name}")
        if desc:
            schema_parts.append(f"Description: {desc}\n")
        schema_parts.append(generate_table_schema(df, df_name))

    # Add relationships
    schema_parts.append("\n# Table Relationships")
    schema_parts.append("- invoices_df.client_id -> clients_df.client_id")
    schema_parts.append("- line_items_df.invoice_id -> invoices_df.invoice_id")

    # Add computed column hints
    schema_parts.append("\n# Computed Values")
    schema_parts.append("- Line item subtotal: quantity * unit_price")
    schema_parts.append("- Line item total with tax: quantity * unit_price * (1 + tax_rate)")

    return "\n".join(schema_parts)
