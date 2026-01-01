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
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown(
    """
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }

    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #1f2937;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }

    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] li {
        color: #1f2937 !important;
    }

    /* Hide chat avatars */
    [data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessage"] .stChatMessageAvatar,
    [data-testid="stChatMessage"] > div:first-child > div:first-child {
        display: none !important;
    }

    /* User message */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #f0f4ff;
        border-color: #c7d2fe;
    }

    [data-testid="stChatMessage"][data-testid*="user"] p,
    [data-testid="stChatMessage"][data-testid*="user"] span,
    [data-testid="stChatMessage"][data-testid*="user"] div {
        color: #1e3a5f !important;
    }

    /* Sample question buttons */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        background-color: white !important;
        color: #374151 !important;
        transition: all 0.2s ease;
        font-size: 0.875rem;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #667eea;
        background-color: #f0f4ff !important;
        color: #4338ca !important;
        transform: translateX(4px);
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: #374151 !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover p {
        color: #4338ca !important;
    }

    /* Expander styling */
    [data-testid="stExpander"] {
        background-color: #f8f9fa !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] > div {
        background-color: #f8f9fa !important;
    }

    [data-testid="stExpander"] summary {
        background-color: #f8f9fa !important;
        border-radius: 8px;
        font-weight: 500;
    }

    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: #374151 !important;
    }

    /* Expander content area */
    [data-testid="stExpander"] > div > div {
        background-color: #f8f9fa !important;
    }

    /* Code block styling - force light text on dark background */
    [data-testid="stExpander"] pre,
    [data-testid="stExpander"] [data-testid="stCode"],
    [data-testid="stExpander"] .stCodeBlock,
    .stCodeBlock pre,
    .stCodeBlock code,
    [data-testid="stCode"] pre,
    [data-testid="stCode"] code {
        background-color: #282c34 !important;
        color: #abb2bf !important;
        border-radius: 8px;
        padding: 1rem !important;
    }

    [data-testid="stExpander"] code,
    [data-testid="stExpander"] pre code,
    .stCodeBlock code,
    [data-testid="stCode"] code {
        color: #abb2bf !important;
        background-color: transparent !important;
    }

    /* Force all text inside code blocks to be visible */
    [data-testid="stExpander"] pre *,
    [data-testid="stExpander"] code *,
    .stCodeBlock pre *,
    .stCodeBlock code *,
    [data-testid="stCode"] * {
        color: #abb2bf !important;
    }

    /* Syntax highlighting colors */
    [data-testid="stExpander"] .token.keyword,
    .stCodeBlock .token.keyword {
        color: #c678dd !important;
    }

    [data-testid="stExpander"] .token.string,
    .stCodeBlock .token.string {
        color: #98c379 !important;
    }

    [data-testid="stExpander"] .token.function,
    .stCodeBlock .token.function {
        color: #61afef !important;
    }

    [data-testid="stExpander"] .token.number,
    .stCodeBlock .token.number {
        color: #d19a66 !important;
    }

    /* Data preview table */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        background-color: white !important;
    }

    /* Dataframe inside expander */
    [data-testid="stExpander"] [data-testid="stDataFrame"] {
        background-color: white !important;
    }

    [data-testid="stExpander"] [data-testid="stDataFrame"] * {
        color: #1f2937 !important;
    }

    /* Table cells */
    [data-testid="stDataFrame"] table {
        background-color: white !important;
    }

    [data-testid="stDataFrame"] th {
        background-color: #f3f4f6 !important;
        color: #374151 !important;
    }

    [data-testid="stDataFrame"] td {
        background-color: white !important;
        color: #1f2937 !important;
    }

    /* Success/Info/Warning messages */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 8px;
    }

    /* Chat input styling */
    [data-testid="stChatInput"] {
        border-radius: 12px;
    }

    [data-testid="stChatInput"] > div {
        border-radius: 12px;
    }

    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #e5e7eb;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hide anchor links on headings */
    a.anchor-link {
        display: none !important;
    }

    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
        pointer-events: none !important;
    }

    [data-testid="stMarkdown"] a[href^="#"] {
        display: none !important;
    }

    /* Loading animation */
    .loading-indicator {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
    }

    .loading-dots {
        display: flex;
        gap: 4px;
    }

    .loading-dots span {
        width: 8px;
        height: 8px;
        background-color: #667eea;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }

    .loading-dots span:nth-child(1) {
        animation-delay: -0.32s;
    }

    .loading-dots span:nth-child(2) {
        animation-delay: -0.16s;
    }

    .loading-dots span:nth-child(3) {
        animation-delay: 0s;
    }

    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0.6);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }

    .loading-text {
        color: #6b7280;
        font-size: 0.9rem;
        font-style: italic;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Data source card styling */
    .data-source-card {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        padding: 0.875rem 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
    }

    .data-source-card-upload {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 0.875rem 1rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
    }

    /* Data source section spacing */
    [data-testid="stSidebar"] [data-testid="stRadio"] {
        margin-bottom: 0;
    }

    /* Radio button styling for data source */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        background-color: white;
        padding: 0.25rem;
        border-radius: 10px;
        border: 1px solid #d1d5db;
        display: flex;
        gap: 0.25rem;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label {
        flex: 1;
        background-color: #f9fafb !important;
        padding: 0.6rem 0.75rem !important;
        border-radius: 8px !important;
        border: 1px solid transparent !important;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label:hover {
        background-color: #f3f4f6 !important;
        border-color: #d1d5db !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label[data-checked="true"] {
        background-color: #667eea !important;
        border-color: #667eea !important;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label p,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label span,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label div {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label[data-checked="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label[data-checked="true"] span,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label[data-checked="true"] div {
        color: white !important;
    }

    /* Hide the radio circle */
    [data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div > label > div:first-child {
        display: none !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar for configuration
with st.sidebar:
    # Logo/Brand section
    st.markdown(
        """
        <div style="text-align: center; padding: 0.5rem 0;">
            <h3 style="margin: 0; color: #667eea;">Data Q&A</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Model Configuration
    st.markdown("## Settings")

    model = st.selectbox(
        "Model",
        options=["claude-sonnet-4-5-20250929", "claude-haiku-4-5-20251001", "claude-opus-4-5-20251101"],
        index=0,
        help="Select the Claude model to use",
    )

    st.markdown("---")

    # Data Source section
    st.markdown("## Data Source")

    # Data source selector with radio buttons for better visibility
    data_source = st.radio(
        "Select data source",
        options=["sample", "upload"],
        format_func=lambda x: "📦 Sample Data" if x == "sample" else "📤 Upload Custom",
        horizontal=True,
        label_visibility="collapsed",
    )

    use_uploaded = data_source == "upload"

    if use_uploaded:
        st.markdown(
            """
            <div class="data-source-card-upload">
                <strong style="color: #92400e;">📤 Custom Data Mode</strong><br>
                <small style="color: #a16207;">Upload your own Excel files below</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_files = st.file_uploader(
            "Upload Excel files",
            type=["xlsx"],
            accept_multiple_files=True,
            help="Each file becomes a queryable table",
            label_visibility="collapsed",
        )

        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) ready")
            with st.expander("View uploaded files", expanded=True):
                for f in uploaded_files:
                    st.markdown(f"📄 `{f.name}`")
        else:
            st.caption("Drop Excel files here or click to browse")
    else:
        uploaded_files = []
        st.markdown(
            """
            <div class="data-source-card">
                <strong style="color: #4338ca;">📦 Sample Dataset Active</strong><br>
                <small style="color: #6366f1;">3 tables: Clients, Invoices, Line Items</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Sample Questions section
    st.markdown("## Try These Questions")

    if use_uploaded and uploaded_files:
        st.caption("Questions depend on your uploaded data")
    else:
        sample_questions = [
            "List all clients with their industries",
            "Which clients are based in the UK?",
            "Invoices issued in March 2024",
            "Which invoices are marked as 'Overdue'?",
            "Count line items by service name",
            "Total billed amount per client in 2024",
            "Client with highest 2024 billing",
        ]

        for q in sample_questions:
            if st.button(q, key=q, width="stretch"):
                st.session_state.selected_question = q

    st.markdown("---")

    # Data Preview section
    st.markdown("## Data Preview")

    if use_uploaded and uploaded_files:
        file_names = [f.name.replace(".xlsx", "") for f in uploaded_files]
        preview_table = st.selectbox("Select table", file_names, label_visibility="collapsed")

        try:
            for f in uploaded_files:
                if f.name.replace(".xlsx", "") == preview_table:
                    df = pd.read_excel(f)
                    break
            st.dataframe(df.head(10), width="stretch", height=200)
            st.caption(f"Showing 10 of {len(df)} rows • {len(df.columns)} columns")
        except Exception as e:
            st.error(f"Could not load data: {e}")
    else:
        preview_table = st.selectbox(
            "Select table",
            ["Clients", "Invoices", "InvoiceLineItems"],
            label_visibility="collapsed",
        )
        try:
            df = pd.read_excel(config.DATA_DIR / f"{preview_table}.xlsx")
            st.dataframe(df.head(10), width="stretch", height=200)
            st.caption(f"Showing 10 of {len(df)} rows • {len(df.columns)} columns")
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
    """Initialize the chat pipeline from the data directory (cached)."""
    return ChatPipeline(data_dir=config.DATA_DIR, api_key=api_key, model=model)


def get_pipeline_from_uploads(api_key: str, model: str, uploaded_files):
    """Initialize the chat pipeline from uploaded files."""
    dataframes = load_uploaded_dataframes(uploaded_files)
    return ChatPipeline(dataframes=dataframes, api_key=api_key, model=model)


# Get API key from config
api_key = config.ANTHROPIC_API_KEY

# Main chat interface
if not api_key:
    # Empty state - no API key
    st.markdown(
        """
        <div style="text-align: center; padding: 4rem 2rem; background-color: #f8f9fa; border-radius: 12px; border: 2px dashed #e5e7eb;">
            <h3 style="margin: 0 0 0.5rem 0; color: #374151;">API Key Required</h3>
            <p style="color: #6b7280; margin: 0;">
                Set your Anthropic API key in the <code>.env</code> file<br>
                <code style="background: #e5e7eb; padding: 0.25rem 0.5rem; border-radius: 4px; margin-top: 0.5rem; display: inline-block;">ANTHROPIC_API_KEY=your-api-key</code>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif use_uploaded and not uploaded_files:
    # Empty state - no files uploaded
    st.markdown(
        """
        <div style="text-align: center; padding: 4rem 2rem; background-color: #f8f9fa; border-radius: 12px; border: 2px dashed #e5e7eb;">
            <h3 style="margin: 0 0 0.5rem 0; color: #374151;">Upload Your Data</h3>
            <p style="color: #6b7280; margin: 0;">Upload at least one Excel file in the sidebar to start querying</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Show available tables info
    if use_uploaded and uploaded_files:
        dataframes = load_uploaded_dataframes(uploaded_files)
        table_names = list(dataframes.keys())
        cols = st.columns(len(table_names))
        for i, name in enumerate(table_names):
            with cols[i]:
                st.metric(
                    label=name.replace("_df", "").replace("_", " ").title(),
                    value=f"{len(dataframes[name])} rows",
                )

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat container
    chat_container = st.container()

    # Display chat history or welcome message
    with chat_container:
        if not st.session_state.messages:
            # Welcome message when no chat history
            st.markdown(
                """
                <div style="text-align: center; padding: 3rem 2rem;">
                    <h3 style="margin: 0 0 0.5rem 0; color: #374151;">Ready to Answer Your Questions</h3>
                    <p style="color: #6b7280; margin: 0 0 1.5rem 0;">
                        Ask questions about your data in plain English.<br>
                        Try a sample question from the sidebar or type your own below.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for message in st.session_state.messages:
                with st.chat_message(message["role"], avatar=None):
                    st.markdown(message["content"])
                    if "code" in message and message["code"]:
                        with st.expander("View generated code", expanded=False):
                            st.code(message["code"], language="python")
                    if "data" in message and message["data"] is not None:
                        with st.expander("View raw data", expanded=False):
                            if isinstance(message["data"], pd.DataFrame):
                                st.dataframe(message["data"], width="stretch")
                            else:
                                st.write(message["data"])

    # Handle selected question from the sidebar
    if "selected_question" in st.session_state:
        question = st.session_state.selected_question
        del st.session_state.selected_question
    else:
        question = None

    # Chat input
    user_input = st.chat_input("Ask a question about your data...")

    # Use either the selected question or user input
    if question or user_input:
        query = question or user_input

        # Add a user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user", avatar=None):
            st.markdown(query)

        # Generate response
        with st.chat_message("assistant", avatar=None):
            # Animated loading indicator
            status_placeholder = st.empty()
            status_placeholder.markdown(
                """
                <div class="loading-indicator">
                    <div class="loading-dots">
                        <span></span><span></span><span></span>
                    </div>
                    <span class="loading-text">Analyzing your question</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            try:
                # Get a pipeline based on a data source
                if use_uploaded and uploaded_files:
                    pipeline = get_pipeline_from_uploads(api_key, model, uploaded_files)
                else:
                    pipeline = get_pipeline_from_dir(api_key, model)

                status_placeholder.markdown(
                    """
                    <div class="loading-indicator">
                        <div class="loading-dots">
                            <span></span><span></span><span></span>
                        </div>
                        <span class="loading-text">Generating response</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                response = pipeline.ask(query)
                status_placeholder.empty()

                # Display answer
                st.markdown(response.answer)

                # Show expandable details
                col1, col2 = st.columns(2)

                with col1:
                    if response.generated_code:
                        with st.expander("View generated code", expanded=False):
                            st.code(response.generated_code, language="python")

                with col2:
                    if response.execution_result.result is not None:
                        with st.expander("View raw data", expanded=False):
                            result = response.execution_result.result
                            if isinstance(result, pd.DataFrame):
                                st.dataframe(result, width="stretch")
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
                status_placeholder.empty()
                error_msg = str(e)
                st.markdown(
                    f"""
                    <div style="background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 1rem; margin-top: 0.5rem;">
                        <strong style="color: #dc2626;">Error</strong>
                        <p style="color: #7f1d1d; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{error_msg}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": f"Error: {error_msg}",
                    }
                )

    # Footer with a clear button
    if st.session_state.messages:
        st.markdown("---")
        col1, col2, col3 = st.columns([4, 2, 4])
        with col2:
            if st.button("Clear Chat", width="stretch"):
                st.session_state.messages = []
                st.rerun()
