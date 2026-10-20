import random
from hangman.constants import MAX_ERRORS,ALPHABET_RU
from enum import Enum


class GuessStatus(Enum):
  CALLED = "Вы уже называли эту букву!"
  RIGHT = "Верно! Буква есть в слове."
  WRONG = "Нет такой буквы. Ошиблись."

class HangmanGame:
    def __init__(self, word):
        self.word = word
        self.alphabet = ALPHABET_RU
        self.letters_state = {}
        
        for letter in self.alphabet:
            self.letters_state[letter] = {
                "in_word": False,
                "indices": [],
                "called": False
            }
        
        for idx, char in enumerate(word):
            self.letters_state[char]["indices"].append(idx)
            self.letters_state[char]["in_word"] = True
            
        self.wrong_count = 0
        self.max_wrong = MAX_ERRORS
    
    def check_guess(self,letter):
        data = self.letters_state[letter]

        if data["called"]:
            return GuessStatus.CALLED

        data["called"] = True
        
        if data["in_word"]:
            return GuessStatus.RIGHT
        else:
            self.wrong_count += 1
            return GuessStatus.WRONG

    def get_masked_word(self):
        masked = ["*"]*len(self.word)

        for char,data in self.letters_state.items():
            if data["called"] and data["in_word"]:
                for index in data["indices"]:
                    masked[index] = char.upper()

        return "".join(masked)

    def is_lost(self):
        return self.wrong_count >= self.max_wrong
    
    def is_won(self):
        return "*" not in self.get_masked_word()