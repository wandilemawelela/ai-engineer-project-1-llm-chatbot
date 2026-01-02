def main():
    """
    Entry point.
    Runs a continuous input loop with clean exit handling.
    """
    while True:
        try:
            user_input = input("You: ")

            # Ignore empty input
            if not user_input.strip():
                continue

            # Exit conditions (case-insensitive)
            if user_input.strip().lower() in {"quit", "exit", "/quit"}:
                print("Goodbye!")
                break

            # Placeholder for LLM call
            # response = call_llm(user_input)
            # print(f"Bot: {response}")

            print("Bot: (LLM response placeholder)")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

