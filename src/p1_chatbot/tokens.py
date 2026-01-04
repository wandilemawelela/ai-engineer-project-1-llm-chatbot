"""
Token counting utilities.

NOTE:
This token count is only an ESTIMATE.

Why?
- Tokenizers are model-specific.
- For non-OpenAI models (e.g., Gemini), we do not have access to the
  exact tokenizer used internally.
- This function uses OpenAI-compatible tokenizers (tiktoken) as a
  reasonable approximation for budgeting and debugging purposes,
  NOT for exact billing accuracy.
"""

import tiktoken


def count_tokens(messages: list[dict[str, str]], model: str) -> int:
    """
    Estimate the number of tokens used by a list of chat messages.

    This function concatenates the `role` and `content` fields of each
    message and counts tokens using tiktoken.

    If the model is unknown to tiktoken, it falls back to the
    `cl100k_base` encoding.

    Args:
        messages: List of chat messages in {role, content} format
        model: Model name (used to select tokenizer)

    Returns:
        Estimated token count as an integer
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    text = ""
    for msg in messages:
        text += f"{msg['role']}: {msg['content']}\n"

    return len(encoding.encode(text))

