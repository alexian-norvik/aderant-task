"""Prompt templates for LLM interactions."""

CODE_GENERATION_PROMPT = """You are a Python data analyst. Given a natural language question about business data, generate pandas code to answer it.

{schema}

# Instructions
1. Write Python code using pandas to answer the question
2. The DataFrames are already loaded and available as: clients_df, invoices_df, line_items_df
3. Store your final result in a variable called `result`
4. Use pandas operations (merge, groupby, filter, etc.) as needed
5. For date filtering, dates are already datetime objects
6. Return ONLY executable Python code, no explanations
7. Do NOT include imports or DataFrame definitions - they are already available

# Examples

Question: "List all clients with their industries"
```python
result = clients_df[["name", "industry"]]
```

Question: "Which clients are based in the UK?"
```python
result = clients_df[clients_df["country"] == "UK"]
```

Question: "Total billed amount per client in 2024"
```python
# Join line items with invoices to get amounts
merged = line_items_df.merge(invoices_df[["invoice_id", "client_id", "invoice_date"]], on="invoice_id")
# Filter for 2024
merged_2024 = merged[merged["invoice_date"].dt.year == 2024]
# Calculate line totals including tax
merged_2024 = merged_2024.copy()
merged_2024["line_total"] = merged_2024["quantity"] * merged_2024["unit_price"] * (1 + merged_2024["tax_rate"])
# Group by client
client_totals = merged_2024.groupby("client_id")["line_total"].sum().reset_index()
# Join with client names
result = client_totals.merge(clients_df[["client_id", "name"]], on="client_id")
```

# Question
{question}

# Code
```python
"""

ANSWER_GENERATION_PROMPT = """You are a helpful assistant answering questions about business data.

Based on the following data retrieved from the database:

{data}

Answer this question in natural language: "{question}"

Guidelines:
- Be precise with all numbers - only report numbers that appear in the data above
- Format currency values appropriately
- If the data is a table, describe it clearly or format it as a readable table
- Keep the answer concise but complete
- If the result is empty or None, say so clearly

Answer:"""
