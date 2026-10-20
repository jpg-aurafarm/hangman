from hangman.io import IOInterface
from hangman.constants import TEXTS, MENU_ART_LOGO, MenuChoiceResult, HANGMAN_ART
from hangman.session import GameSession, GameStepResult, SessionState

class Runner:
    def __init__(self, io: IOInterface, session: GameSession):
        self.io = io
        self.session = session

    def run(self):
        while True:
            state = self.session.state

            if state == SessionState.MENU:
                self.run_menu_step()
            elif state == SessionState.PLAYING:
                self.run_play_step()
            elif state == SessionState.GAME_OVER:
                self.run_game_over_step()                      
            elif state == SessionState.EXIT:
                return
    
    def run_menu_step(self):
        self.io.clear()
        self.io.output(MENU_ART_LOGO)
        self.io.output(TEXTS["menu_1"])
        self.io.output(TEXTS["menu_2"])
        self.io.output(TEXTS["menu_3"])

        raw = self.io.input(TEXTS["menu_prompt"])
        status = self.session.choose_menu(raw)

        if status == MenuChoiceResult.INVALID:
            self.io.output(TEXTS["invalid_menu_choice"])
            self.io.input(TEXTS["invalid_menu_choice_input_prompt"])
        elif status in (MenuChoiceResult.SINGLE, MenuChoiceResult.MARATHON):
            self.session.start_game()
            self.render_game()

    def run_play_step(self):
        raw = self.io.input(TEXTS["input_prompt"])
        result = self.session.submit_guess(raw)

        if result == GameStepResult.INVALID_INPUT:
            self.io.output(TEXTS["input_error_char"])
            return
        elif result == GameStepResult.CALLED_INPUT:
            self.io.output(TEXTS["called_input"]) 
            return
        self.render_game()

    def run_game_over_step(self):
        self.render_game()
        self.io.input(TEXTS["exit_prompt"])
        self.session.back_to_menu()

    def render_game(self):
        view = self.session.get_view()
        self.io.clear()
        self.io.output(view["masked"])
        self.io.output(HANGMAN_ART[view["wrong"]])
        self.io.output(TEXTS["stats_errors"].format(view["wrong"], view["max_wrong"]))
        if view["called_letters"]:
            self.io.output(TEXTS["called_chars"].format(view["called_letters"]))
        else:
            self.io.output(TEXTS["called_empty"])
        if view["won"]:
            self.io.output(TEXTS["win"])
        elif view["lost"]:
            self.io.output(TEXTS["lose"].format(view["word"]))
