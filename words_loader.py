from hangman.constants import DEFAULT_WORDS


def load_words(filename: str = "words.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
            return words if words else DEFAULT_WORDS
    except FileNotFoundError:
        return DEFAULT_WORDS