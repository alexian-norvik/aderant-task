# Setup Guide

## Prerequisites

- **Python 3.11+**
- **uv** package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Anthropic API key** ([get one here](https://console.anthropic.com/))

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd aderant-task
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## Data Options

You have two options for data:

### Option A: Upload Your Own Data

If you have your own Excel files, you can upload them directly in the app:

1. Start the app (see below)
2. Toggle **"Upload custom files"** in the sidebar
3. Upload one or more `.xlsx` files
4. Each file becomes a queryable table (e.g., `Sales.xlsx` → `sales_df`)

**Supported format:** Any Excel file with tabular data. Date columns are auto-detected.

### Option B: Generate Sample Data

If you don't have data, generate sample business data:

```bash
uv run python scripts/generate_sample_data.py
```

This creates Excel files in the `data/` directory:
- `Clients.xlsx` (10 clients)
- `Invoices.xlsx` (31 invoices)
- `InvoiceLineItems.xlsx` (89 line items)

The sample data simulates a legal services business with clients, invoices, and billable services.

## Running the Application

### Start the Streamlit app

```bash
uv run streamlit run app.py
```

The app will open automatically in your browser at: **http://localhost:8501**

### Using the Chat Interface

1. Enter your API key in the sidebar (if not set in `.env`)
2. Select a model from the dropdown
3. Choose your data source:
   - **Default:** Uses sample data from `data/` directory
   - **Upload:** Toggle "Upload custom files" to use your own Excel files
4. Type a question or click a sample question from the sidebar
5. View the answer, generated code, and raw data

## Running Tests

```bash
uv run pytest tests/ -v
```

## Example Questions

### For Sample Data

- "List all clients with their industries"
- "Which clients are based in the UK?"
- "Which invoices are currently marked as Overdue?"
- "For each client, compute the total amount billed in 2024 (including tax)"
- "Which client has the highest total billed amount in 2024?"

### For Your Own Data

Ask questions relevant to your uploaded files. The system will show available table names after upload.

Examples:
- "Show all records from [table_name]"
- "What are the column names in [table_name]?"
- "Group [column] by [another_column] and show totals"

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

Make sure your `.env` file exists and contains a valid API key:

```bash
cat .env
# Should show: ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### "No module named 'src'"

Run the app from the project root directory:

```bash
cd aderant-task
uv run streamlit run app.py
```

### Port 8501 already in use

Kill the existing process or use a different port:

```bash
uv run streamlit run app.py --server.port 8502
```

### Uploaded file not recognized

Make sure your file:
- Is in `.xlsx` format (Excel)
- Contains tabular data with headers in the first row
- Has no password protection
