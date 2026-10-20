from hangman.io import ConsoleIO
from hangman.session import GameSession
from hangman.runner import Runner
from words_loader import load_words


def main():
    io = ConsoleIO()
    words = load_words("words.txt")
    session = GameSession(words)
    runner = Runner(io, session)
    runner.run()


if __name__ == "__main__":
    main()