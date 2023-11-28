from .playercontroller import PlayerMenuController
from .homecontroller import HomeController
from .tournamentcontroller import TournamentMenuController
from .endcontroller import EndController


class ApplicationController:
    """Controller for the app itself."""

    def __init__(self):
        self.current_controller = HomeController()
        self.home = HomeController()
        self.players_menu = PlayerMenuController()
        self.tournament_handling_menu = TournamentMenuController()
        self.end_controller = EndController()

    def start(self):
        """Starts the app and handle keyboard interruptions."""
        self.current_controller.view.print_welcome()

        try:
            while self.current_controller:
                next_controller = self.current_controller.run()
                if next_controller == "home":
                    self.current_controller = self.home
                elif next_controller == "players_menu":
                    self.current_controller = self.players_menu
                elif next_controller == "tournament_menu":
                    self.current_controller = self.tournament_handling_menu
                else:
                    self.current_controller = self.end_controller
        except KeyboardInterrupt:
            self.current_controller = self.end_controller.hard_stop()
