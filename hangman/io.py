from typing import Protocol
import os

class IOInterface(Protocol):
    def input(self, prompt: str = ""):
        ...
    def output(self, text: str):
        ...
    def clear(self):
        ...

class ConsoleIO(IOInterface):
    def input(self, prompt: str = ""):
        return input(prompt)
    def output(self, text: str):
        print(text)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')