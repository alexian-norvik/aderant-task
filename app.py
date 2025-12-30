"""Streamlit chat interface for the RAG system."""

import pandas as pd
import streamlit as st

import config
from src.chat import ChatPipeline

# Page configuration
st.set_page_config(
    page_title="Tabular Data Q&A",
    page_icon="📊",
    layout="wide",
)

# Title
st.title("📊 Chat Over Tabular Data")
st.markdown("Ask questions about your data in natural language.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")

    api_key = st.text_input(
        "Anthropic API Key",
        value=config.ANTHROPIC_API_KEY,
        type="password",
        help="Enter your Anthropic API key or set ANTHROPIC_API_KEY environment variable",
    )

    model = st.selectbox(
        "Model",
        options=[config.DEFAULT_MODEL, "claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"],
        index=0,
    )

    st.divider()

    # File upload section
    st.header("Data Source")

    use_uploaded = st.toggle("Upload custom files", value=False)

    if use_uploaded:
        uploaded_files = st.file_uploader(
            "Upload Excel files",
            type=["xlsx"],
            accept_multiple_files=True,
            help="Upload one or more Excel files. Each file becomes a queryable table.",
        )

        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) uploaded!")
            for f in uploaded_files:
                st.caption(f"• {f.name}")
        else:
            st.info("Upload Excel files to query your own data.")
    else:
        uploaded_files = []
        st.info("Using sample data from `data/` directory")

    st.divider()

    st.header("Sample Questions")

    if use_uploaded and uploaded_files:
        st.markdown("*Questions depend on your uploaded data*")
    else:
        sample_questions = [
            "List all clients with their industries.",
            "Which clients are based in the UK?",
            "List all invoices issued in March 2024 with their statuses.",
            "Which invoices are currently marked as 'Overdue'?",
            "For each service_name in InvoiceLineItems, how many line items are there?",
            "For each client, compute the total amount billed in 2024 (including tax).",
            "Which client has the highest total billed amount in 2024?",
        ]

        for q in sample_questions:
            if st.button(q[:50] + "..." if len(q) > 50 else q, key=q):
                st.session_state.selected_question = q

    st.divider()

    # Show data preview
    st.header("Data Preview")

    if use_uploaded and uploaded_files:
        # Preview uploaded files
        file_names = [f.name.replace(".xlsx", "") for f in uploaded_files]
        preview_table = st.selectbox("Select table", file_names)

        try:
            # Find the matching file
            for f in uploaded_files:
                if f.name.replace(".xlsx", "") == preview_table:
                    df = pd.read_excel(f)
                    break
            st.dataframe(df.head(10), width="stretch")
            st.caption(f"Showing 10 of {len(df)} rows")
        except Exception as e:
            st.error(f"Could not load data: {e}")
    else:
        # Preview sample data
        preview_table = st.selectbox(
            "Select table",
            ["Clients", "Invoices", "InvoiceLineItems"],
        )
        try:
            df = pd.read_excel(config.DATA_DIR / f"{preview_table}.xlsx")
            st.dataframe(df.head(10), width="stretch")
            st.caption(f"Showing 10 of {len(df)} rows")
        except Exception as e:
            st.error(f"Could not load data: {e}")


def load_uploaded_dataframes(uploaded_files) -> dict[str, pd.DataFrame]:
    """Load dataframes from uploaded files."""
    dataframes = {}
    for f in uploaded_files:
        # Create DataFrame name from filename (e.g., "Clients.xlsx" -> "clients_df")
        name = f.name.replace(".xlsx", "").lower().replace(" ", "_") + "_df"

        # Try to detect date columns and parse them
        df = pd.read_excel(f)

        # Auto-detect date columns by name
        for col in df.columns:
            col_lower = col.lower()
            if "date" in col_lower or col_lower.endswith("_at") or col_lower.endswith("_on"):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass  # Keep as-is if conversion fails

        dataframes[name] = df

    return dataframes


# Initialize chat pipeline
@st.cache_resource
def get_pipeline_from_dir(api_key: str, model: str):
    """Initialize the chat pipeline from data directory (cached)."""
    return ChatPipeline(data_dir=config.DATA_DIR, api_key=api_key, model=model)


def get_pipeline_from_uploads(api_key: str, model: str, uploaded_files):
    """Initialize the chat pipeline from uploaded files."""
    dataframes = load_uploaded_dataframes(uploaded_files)
    return ChatPipeline(dataframes=dataframes, api_key=api_key, model=model)


# Main chat interface
if not api_key:
    st.warning("Please enter your Anthropic API key in the sidebar to start chatting.")
elif use_uploaded and not uploaded_files:
    st.warning("Please upload at least one Excel file in the sidebar to start chatting.")
else:
    # Show available tables info
    if use_uploaded and uploaded_files:
        dataframes = load_uploaded_dataframes(uploaded_files)
        table_info = ", ".join([f"`{name}`" for name in dataframes.keys()])
        st.info(f"Available tables: {table_info}")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "code" in message and message["code"]:
                with st.expander("View generated code"):
                    st.code(message["code"], language="python")
            if "data" in message and message["data"] is not None:
                with st.expander("View raw data"):
                    if isinstance(message["data"], pd.DataFrame):
                        st.dataframe(message["data"])
                    else:
                        st.write(message["data"])

    # Handle selected question from sidebar
    if "selected_question" in st.session_state:
        question = st.session_state.selected_question
        del st.session_state.selected_question
    else:
        question = None

    # Chat input
    user_input = st.chat_input("Ask a question about the data...")

    # Use either the selected question or user input
    if question or user_input:
        query = question or user_input

        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data..."):
                try:
                    # Get pipeline based on data source
                    if use_uploaded and uploaded_files:
                        pipeline = get_pipeline_from_uploads(api_key, model, uploaded_files)
                    else:
                        pipeline = get_pipeline_from_dir(api_key, model)

                    response = pipeline.ask(query)

                    # Display answer
                    st.markdown(response.answer)

                    # Show code
                    if response.generated_code:
                        with st.expander("View generated code"):
                            st.code(response.generated_code, language="python")

                    # Show raw data
                    if response.execution_result.result is not None:
                        with st.expander("View raw data"):
                            result = response.execution_result.result
                            if isinstance(result, pd.DataFrame):
                                st.dataframe(result)
                            else:
                                st.write(result)

                    # Store in history
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response.answer,
                            "code": response.generated_code,
                            "data": response.execution_result.result
                            if isinstance(response.execution_result.result, pd.DataFrame | pd.Series)
                            else None,
                        }
                    )

                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_msg,
                        }
                    )

    # Clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
