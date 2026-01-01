import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("GOOGLE_API_KEY not found in environment", file=sys.stderr)
        sys.exit(1)

    # Create a client with the API key
    client = genai.Client(api_key=api_key)

    # Exact prompt required
    prompt = (
        "Explain the difference between an AI Engineer and a Software Engineer "
        "in one sentence."
    )

    try:
        # Make a single LLM request
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # a valid text generation model
            contents=prompt
        )

        # Print only the text output
        print(response.text.strip())

        # Exit with status code 0 (success)
        sys.exit(0)

    except Exception as e:
        # If something goes wrong, print error and exit non-zero
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

