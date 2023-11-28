from .baseview import BaseView


class HomeView(BaseView):
    """View of the main menu."""

    def render(self):
        self.print_header("MENU PRINCIPAL")
        print(
            "1. Lister les tournois existants.\n"
            "2. Créer un tournoi.\n"
            "3. Sélectionner et jouer un tournoi.\n"
            "4. Gestion des joueurs.\n"
            "9. Quitter le programme.\n"
        )

    def print_welcome(self):
        print(
            "Tournament manager v.0.10.0.\n"
            "Read README.md."
            )

    def get_name(self):
        return input("Nom du tournoi : ")

    def get_location(self):
        return input("Lieu du tournoi : ")

    def get_start_date(self):
        return input("Date de début du tournoi (au format JJ/MM/AAAA): ")

    def get_end_date(self):
        return input("Date de fin du tournoi (au format JJ/MM/AAAA). : ")

    def get_time_control(self):
        return input("Type de contrôle du temps (peut être 'bullet', 'blitz' ou 'fast') : ")

    def get_description(self):
        return input("(optional) Description : ")
