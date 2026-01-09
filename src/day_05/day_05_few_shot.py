import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def main():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model_name = "gemini-2.5-flash"

    # EXACTLY 3 labeled examples (few-shot)
    contents = [
        genai.types.Content(
            role="user",
            parts=[genai.types.Part(text="I loved this movie. Great pacing and strong acting.")]
        ),
        genai.types.Content(
            role="model",
            parts=[genai.types.Part(text="Positive")]
        ),
        genai.types.Content(
            role="user",
            parts=[genai.types.Part(text="Not worth my time. The plot was confusing and boring.")]
        ),
        genai.types.Content(
            role="model",
            parts=[genai.types.Part(text="Negative")]
        ),
        genai.types.Content(
            role="user",
            parts=[genai.types.Part(text="Surprisingly good. I would watch it again.")]
        ),
        genai.types.Content(
            role="model",
            parts=[genai.types.Part(text="Positive")]
        ),
        # Unlabeled test review
        genai.types.Content(
            role="user",
            parts=[genai.types.Part(
                text="The cinematography was nice but the story felt flat and predictable."
            )]
        ),
    ]

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
    )

    # Output EXACTLY one label
    print(response.text.strip())

if __name__ == "__main__":
    main()
