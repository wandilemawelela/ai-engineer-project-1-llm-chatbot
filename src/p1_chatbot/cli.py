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
    Truncate oldest user/assistant pairs while preserving the system prompt.
    """
    while True:
        estimated_input_tokens = count_tokens(messages, model_name)

        if estimated_input_tokens + RESERVED_OUTPUT_TOKENS <= EXERCISE_MAX_CONTEXT_TOKENS:
            break

        # Never remove the system prompt
        if len(messages) <= 1:
            break

        # Handle malformed history safely
        if messages[1].get("role") != "user":
            messages.pop(1)
            print("[context] Truncated malformed message to restore order.")
            continue

        # Remove oldest user + assistant pair
        removed = False

        if len(messages) > 1:
            messages.pop(1)
            removed = True

        if len(messages) > 1 and messages[1].get("role") == "assistant":
            messages.pop(1)
            removed = True

        if removed:
            print("[context] Truncated oldest messages to fit token budget.")
        else:
            break


def main():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model_name = "gemini-2.5-flash"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    cot_enabled = False

    print("System prompt loaded. Type /quit to exit.")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Exit commands
            if user_input.lower() in {"quit", "exit", "/quit"}:
                print("Goodbye!")
                break

            # CoT toggle command
            if user_input.lower() == "/cot":
                cot_enabled = True
                print("[mode] CoT enabled for next turn.")
                continue

            # Apply CoT instruction once
            if cot_enabled:
                user_input = (
                    "Explain your reasoning step-by-step, then give the final answer.\n\n"
                    + user_input
                )

            messages.append({"role": "user", "content": user_input})

            input_tokens_estimate = count_tokens(messages, model_name)
            print(f"Tokens (estimated input): {input_tokens_estimate}")

            truncate_history_if_needed(messages, model_name)

            contents = [
                genai.types.Content(
                    role="user" if msg["role"] == "user" else "model",
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

            # Disable CoT after one use
            if cot_enabled:
                cot_enabled = False
                print("[mode] CoT disabled.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"[error] {e}")


if __name__ == "__main__":
    main()
