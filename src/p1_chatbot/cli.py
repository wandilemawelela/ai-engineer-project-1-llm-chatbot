import os
from dotenv import load_dotenv
from google import genai

from tokens import count_tokens
from prompts import SYSTEM_PROMPT

EXERCISE_MAX_CONTEXT_TOKENS = 4096
RESERVED_OUTPUT_TOKENS = 500
TRUNCATE_THRESHOLD_TOKENS = 3500

load_dotenv()


def truncate_history_if_needed(messages, model_name):
    """
    Truncate conversation history while preserving the system prompt
    at index 0. Removes oldest user/assistant pairs starting from index 1.
    """
    while True:
        estimated_input_tokens = count_tokens(messages, model_name)

        if estimated_input_tokens + RESERVED_OUTPUT_TOKENS <= EXERCISE_MAX_CONTEXT_TOKENS:
            break

        # Never remove the system prompt
        if len(messages) <= 1:
            break

        # If history is malformed after system prompt, remove one message at a time
        if messages[1].get("role") == "assistant":
            messages.pop(1)
            print("[context] Truncated malformed message to restore order.")
            continue

        removed_any = False

        # Remove oldest user message (index 1)
        if len(messages) > 1:
            messages.pop(1)
            removed_any = True

        # Remove corresponding assistant message if present
        if len(messages) > 1 and messages[1].get("role") == "assistant":
            messages.pop(1)
            removed_any = True

        if removed_any:
            print("[context] Truncated oldest messages to fit token budget.")
        else:
            break


def main():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model_name = "gemini-2.5-flash"

    # Initialize messages with system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("System prompt loaded. Type /quit to exit.")

    while True:
        try:
            user_input = input("You: ")

            if not user_input.strip():
                continue

            if user_input.strip().lower() in {"quit", "exit", "/quit"}:
                print("Goodbye!")
                break

            messages.append({"role": "user", "content": user_input})

            input_tokens_estimate = count_tokens(messages, model_name)
            print(f"Tokens (estimated input): {input_tokens_estimate}")

            truncate_history_if_needed(messages, model_name)

            contents = [
                genai.types.Content(
                    role="user" if msg["role"] in {"user", "system"} else "model",
                    parts=[genai.types.Part(text=msg["content"])]
                )
                for msg in messages
            ]

            response = client.models.generate_content(
                model=model_name,
                contents=contents,
            )

            assistant_text = response.text.strip()
            print(f"Assistant: {assistant_text}")

            messages.append({"role": "assistant", "content": assistant_text})

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"[error] {e}")


if __name__ == "__main__":
    main()