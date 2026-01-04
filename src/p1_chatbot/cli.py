import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from tokens import count_tokens


load_dotenv()


def main():
    """
    Entry point for the p1_chatbot CLI using Google Gemini.
    """

    model_name = "gemini-2.5-flash"

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    messages: list[dict[str, str]] = []

    while True:
        try:
            user_input = input("You: ")

            if not user_input.strip():
                continue

            if user_input.strip().lower() in {"quit", "exit", "/quit"}:
                print("Goodbye!")
                break

            messages.append({
                "role": "user",
                "content": user_input
            })

            # 🔹 Estimate tokens BEFORE API call
            input_tokens_estimate = count_tokens(messages, model_name)
            print(f"Tokens (estimated input): {input_tokens_estimate}")

            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])]
                    )
                )

            response = client.models.generate_content(
                model=model_name,
                contents=contents,
            )

            assistant_text = response.text.strip()
            print(f"Assistant: {assistant_text}")

            messages.append({
                "role": "assistant",
                "content": assistant_text
            })

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

