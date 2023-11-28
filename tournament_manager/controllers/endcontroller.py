from tournament_manager.views import EndView


class EndController:
    """Controller handling app closure."""

    def __init__(self):
        self.view = EndView()

    def run(self):
        self.view.render()
        choice = self.view.confirm_exit()
        if choice.upper() == "Y":
            exit()
        elif choice.upper() == "N":
            return "home"
        else:
            self.view.notify_invalid_choice()
            self.view.cancelled()
            return "home"

    def hard_stop(self):
        self.view.alert_user("\nFermeture au clavier. Au revoir !")
        return None
