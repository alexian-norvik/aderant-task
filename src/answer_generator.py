"""Generate natural language answers from query results."""

import anthropic
import pandas as pd

from .common.llm_constants import DEFAULT_MODEL, MAX_TOKENS
from .common.prompt_templates import ANSWER_GENERATION_PROMPT


class AnswerGenerator:
    """Generate natural language answers from query results."""

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, question: str, result: object, code: str) -> str:
        """Generate a natural language answer from the query result."""
        # Format the result for the prompt
        data_str = self._format_result(result)

        prompt = ANSWER_GENERATION_PROMPT.format(data=data_str, question=question)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text.strip()

    def _format_result(self, result: object) -> str:
        """Format the result for display in the prompt."""
        if result is None:
            return "No data returned"

        if isinstance(result, pd.DataFrame):
            if len(result) == 0:
                return "Empty DataFrame (no matching records)"
            if len(result) > 50:
                return f"DataFrame with {len(result)} rows:\n{result.head(50).to_string()}\n... (truncated)"
            return result.to_string()

        if isinstance(result, pd.Series):
            if len(result) == 0:
                return "Empty Series (no matching records)"
            return result.to_string()

        # Scalar or other types
        return str(result)
