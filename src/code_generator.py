"""Generate pandas code using Claude LLM."""

import anthropic

from .common.llm_constants import DEFAULT_MODEL, MAX_TOKENS
from .common.prompt_templates import CODE_GENERATION_PROMPT


class CodeGenerator:
    """Generate pandas code using Claude API."""

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, question: str, schema: str) -> str:
        """Generate pandas code to answer the question."""
        prompt = CODE_GENERATION_PROMPT.format(schema=schema, question=question)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        # Extract code from response (handle markdown code blocks)
        code = self._extract_code(response_text)
        return code

    def _extract_code(self, text: str) -> str:
        """Extract Python code from response text."""
        # If response contains code blocks, extract the code
        if "```python" in text:
            start = text.find("```python") + len("```python")
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()

        if "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()

        # Otherwise return the text as-is (assuming it's just code)
        return text.strip()
