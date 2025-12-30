"""Main chat orchestration for the RAG pipeline."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .answer_generator import AnswerGenerator
from .code_generator import CodeGenerator
from .common.llm_constants import DEFAULT_MODEL
from .data_loader import DataLoader
from .executor import ExecutionResult, SafeCodeExecutor
from .schema import generate_full_schema


@dataclass
class ChatResponse:
    """Response from the chat pipeline."""

    answer: str
    generated_code: str
    execution_result: ExecutionResult
    success: bool
    error: str | None = None


class ChatPipeline:
    """Main RAG pipeline for tabular data Q&A."""

    def __init__(
        self,
        data_dir: Path | str | None = None,
        dataframes: dict[str, pd.DataFrame] | None = None,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
    ):
        # Load dataframes either from directory or use provided ones
        if dataframes is not None:
            self.dataframes = dataframes
        elif data_dir is not None:
            self.data_dir = Path(data_dir)
            self.data_loader = DataLoader(self.data_dir)
            self.dataframes = self.data_loader.load_all()
        else:
            raise ValueError("Either data_dir or dataframes must be provided")

        # Initialize components
        self.schema = generate_full_schema(self.dataframes)
        self.code_generator = CodeGenerator(api_key=api_key, model=model)
        self.executor = SafeCodeExecutor(self.dataframes)
        self.answer_generator = AnswerGenerator(api_key=api_key, model=model)

    def ask(self, question: str, max_retries: int = 2) -> ChatResponse:
        """Process a question through the RAG pipeline."""
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                # Step 1: Generate code
                if attempt == 0:
                    code = self.code_generator.generate(question, self.schema)
                else:
                    # Include previous error in retry prompt
                    error_context = f"\n\nPrevious attempt failed with error: {last_error}\nPlease fix the code."
                    code = self.code_generator.generate(question + error_context, self.schema)

                # Step 2: Execute code
                exec_result = self.executor.execute(code)

                if not exec_result.success:
                    last_error = exec_result.error
                    continue

                # Step 3: Generate natural language answer
                answer = self.answer_generator.generate(question, exec_result.result, code)

                return ChatResponse(
                    answer=answer,
                    generated_code=code,
                    execution_result=exec_result,
                    success=True,
                )

            except Exception as e:
                last_error = str(e)
                continue

        # All retries failed
        return ChatResponse(
            answer=f"I wasn't able to answer that question. Error: {last_error}",
            generated_code=code if "code" in locals() else "",
            execution_result=exec_result
            if "exec_result" in locals()
            else ExecutionResult(success=False, error=last_error),
            success=False,
            error=last_error,
        )

    def get_schema(self) -> str:
        """Get the database schema description."""
        return self.schema
