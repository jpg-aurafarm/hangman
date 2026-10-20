import random
from enum import Enum
from hangman.game import HangmanGame,GuessStatus
from hangman.constants import MenuChoiceResult, HANGMAN_ART, ALPHABET_RU

class GameStepResult(Enum):
    CONTINUE = "continue"
    WON = "won"
    LOST = "lost"
    INVALID_INPUT = "invalid_input"
    CALLED_INPUT = "called_input"

class SessionState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    EXIT = "exit"

class GameMode(Enum):
    SINGLE = "single" #Одна игра и выход
    MARATHON = "marathon" #Игра -> Меню


class GameSession:
    def __init__(self, words_list: list[str]):
        self.words_list = words_list
        self.state = SessionState.MENU
        self.game: HangmanGame | None = None
        self.mode = GameMode.SINGLE

    def choose_menu(self, raw: str) -> MenuChoiceResult:
        raw = raw.strip().lower()
        if raw == "1":
            self.mode = GameMode.MARATHON
            return MenuChoiceResult.MARATHON
        if raw == "2":
            self.mode = GameMode.SINGLE
            return MenuChoiceResult.SINGLE
        if raw == "3":
            self.state = SessionState.EXIT
            return MenuChoiceResult.EXIT
        return MenuChoiceResult.INVALID

    
    def start_game(self):
        self.game = HangmanGame(random.choice(self.words_list))
        self.state = SessionState.PLAYING

    def back_to_menu(self):
        if self.mode == GameMode.MARATHON:
            self.state = SessionState.MENU
        else:
            self.state = SessionState.EXIT
    
    def submit_guess(self, raw: str):
        if self.state != SessionState.PLAYING or self.game is None:
            return GameStepResult.INVALID_INPUT

        if len(raw) != 1:
            return GameStepResult.INVALID_INPUT
        ch = raw.lower()
        if ch not in ALPHABET_RU:
            return GameStepResult.INVALID_INPUT

        
        guess_result = self.game.check_guess(ch)
        if guess_result == GuessStatus.CALLED:
            return GameStepResult.CALLED_INPUT


        if self.game.is_won():
            self.state = SessionState.GAME_OVER
            return GameStepResult.WON
        if self.game.is_lost():
            self.state = SessionState.GAME_OVER
            return GameStepResult.LOST
        
        return GameStepResult.CONTINUE
# ==========
    def get_view(self):
        if self.game is None:
            return None
            
        called = sorted(ch for ch, d in self.game.letters_state.items() if d["called"])
        return {
            "state": self.state.value,
            "masked": self.game.get_masked_word(),
            "wrong": self.game.wrong_count,
            "max_wrong": self.game.max_wrong,
            "hangman_art": HANGMAN_ART[self.game.wrong_count],
            "called_letters": called,
            "won": self.game.is_won(),
            "lost": self.game.is_lost(),
            "word": self.game.word if self.game.is_lost() else None
        }