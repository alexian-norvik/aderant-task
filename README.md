# Tabular Data RAG System

A RAG-style question-answering system for querying tabular business data using natural language.

## How to Run

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd aderant-task

# Install dependencies
uv sync

# Generate sample data (if not already present)
uv run python scripts/generate_sample_data.py

# Set your API key (option 1: environment variable)
export ANTHROPIC_API_KEY=your-api-key-here

# Or (option 2: .env file)
cp .env.example .env
# Then edit .env and add your API key

# Run the Streamlit app
uv run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## High-Level Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  User       │────▶│  Schema Context  │────▶│  Claude API │
│  Question   │     │  + Question      │     │  (Code Gen) │
└─────────────┘     └──────────────────┘     └──────┬──────┘
                                                    │
                    ┌──────────────────┐            │ Generated
                    │  Safe Executor   │◀───────────┘ Pandas Code
                    │  (sandboxed)     │
                    └────────┬─────────┘
                             │ Query Results
                             ▼
                    ┌──────────────────┐     ┌─────────────┐
                    │  Results +       │────▶│  Claude API │────▶ Natural Language
                    │  Original Query  │     │  (Answer)   │      Answer
                    └──────────────────┘     └─────────────┘
```

### Key Components

1. **Data Loader** (`src/aderant_task/data_loader.py`)
   - Loads Excel files into pandas DataFrames
   - Handles date parsing for invoice dates

2. **Schema Generator** (`src/aderant_task/schema.py`)
   - Creates human-readable schema descriptions
   - Includes column types, sample values, and relationships

3. **Code Generator** (`src/aderant_task/code_generator.py`)
   - Uses Claude to generate pandas code from natural language
   - Includes few-shot examples for common query patterns

4. **Safe Executor** (`src/aderant_task/executor.py`)
   - AST-based validation to block dangerous operations
   - Sandboxed execution environment
   - Returns execution results or errors

5. **Answer Generator** (`src/aderant_task/answer_generator.py`)
   - Converts query results to natural language
   - Ensures answers are grounded in actual data

6. **Chat Pipeline** (`src/aderant_task/chat.py`)
   - Orchestrates the entire RAG pipeline
   - Handles retries on code generation failures

### Why Text-to-Code (not Vector RAG)?

Traditional RAG embeds text chunks and retrieves semantically similar content. This doesn't work well for tabular data because:

- Questions like "total billed amount including tax" require **calculations**
- Aggregations (GROUP BY, SUM) don't work with chunk retrieval
- JOINs across tables need **structured queries**

Our approach generates pandas code, executes it, and uses the **actual results** to generate answers. This ensures:

- **Zero hallucination** for numbers (all values come from executed code)
- Support for complex aggregations and multi-table queries
- Transparent and verifiable results

## Project Structure

```
aderant-task/
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Excel file loading
│   ├── schema.py               # Schema generation
│   ├── code_generator.py       # LLM code generation
│   ├── executor.py             # Safe code execution
│   ├── answer_generator.py     # NL answer generation
│   ├── chat.py                 # Pipeline orchestration
│   └── common/
│       ├── __init__.py
│       ├── constants.py        # General constants
│       ├── llm_constants.py    # LLM configuration
│       └── prompt_templates.py # Prompt templates
├── data/                       # Excel data files
│   ├── Clients.xlsx
│   ├── Invoices.xlsx
│   └── InvoiceLineItems.xlsx
├── scripts/
│   └── generate_sample_data.py # Sample data generator
├── tests/
│   └── test_pipeline.py        # Unit tests
├── app.py                      # Streamlit interface
├── config.py                   # Centralized configuration
├── .env.example                # Environment variables template
├── results.md                  # Test results
├── pyproject.toml
└── README.md
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| LLM | Claude 3.5 Sonnet (Anthropic) |
| Data Processing | pandas |
| Excel Reading | openpyxl |
| Web Interface | Streamlit |
| Package Manager | uv |
| Code Quality | ruff, pre-commit |
