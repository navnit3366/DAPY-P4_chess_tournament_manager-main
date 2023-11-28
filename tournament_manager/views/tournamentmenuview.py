from tournament_manager.models.tournament import SCORE_DRAW
from .baseview import BaseView


class TournamentHomeView(BaseView):

    def render(self, current_tournament):
        self.print_header("MENU DES TOURNOIS")
        if current_tournament is not None:
            print(f'Current tournament : {current_tournament.name}\n')
        else:
            print('Current tournament : None\n')
        print(
            "1. Sélectionner un tournoi / changer de tournoi sélectionné.\n"
            "2. Ajouter des joueurs au tournoi.\n"
            "3. Commencer un nouveau tour de jeu.\n"
            "4. Entrer les résultats d'un tour entamé.\n"
            "5. Lister les joueurs du tournoi.\n"
            "6. Lister les tours du tournoi.\n"
            "7. Lister les matchs du tournoi.\n"
            "0. Retour au menu principal.\n"
            "9. Quitter le programme."
        )

    # ROUND RELATED METHODS
    def print_round_header(self):
        print("Nom\t   Date de debut\t\t Date de fin\t\t\tMatch 1\t\t\tMatch 2\t\t\tMatch 3\t\t\tMatch 4")

    def print_round_details(self, round):
        details = (
            f'{round.name}    '
            f'{round.start_datetime}    ')
        # Slightly modify display if round is unfinished
        if round.end_datetime is not None:
            details += f'{round.end_datetime}\t'
        else:
            details += "-\t\t\t\t"
        for match in round.matchs:
            if round.end_datetime is not None:
                details += f'{match[0][0]} ({match[0][1]}) vs {match[1][0]} ({match[1][1]})\t'
            else:
                details += f'{match[0][0]} (?) vs {match[1][0]} (?)  \t'
        print(details)
        return None

    @staticmethod
    def print_round_ended(round):
        round_name = round.name
        end_date = round.end_datetime
        print(f'{round_name} terminé le {end_date}.')

    @staticmethod
    def cant_start_round():
        print("Un nouveau tour ne peut pas commencer: en attente de nouveaux résultats ou maximum de tours atteint.")

    # MATCH RELATED METHODS
    def print_match_header(self):
        print(
            "\tNoirs\t"
            "Blancs\t"
            "Gagnant.e"
        )

    def print_match_details(self, match):
        player_black = match[0][0]
        score_black = match[0][1]
        player_white = match[1][0]
        score_white = match[1][1]
        if score_black == "-" and score_white == "-":
            winner = "Match non joué"
        elif score_black == SCORE_DRAW and score_white == SCORE_DRAW:
            winner = "Egalité"
        elif score_black > score_white:
            winner = player_black
        else:
            winner = player_white
        print(f"\t{player_black}\t{player_white}\t{winner}")

    def get_match_score(self, player_id):
        try:
            return float(input(f"Score du joueur {player_id} : "))
        except ValueError:
            print("Score doit être un nombre.")
            return self.get_match_score(player_id)

    # ALL MANNERS OF ERRORS
    def print_reached_max_rounds(self, max_round):
        print(f"Le nombre de tour par tournoi ne peut pas excéder {max_round}.")

    def no_tournament_in_database(self):
        print("Aucun tournoi dans la base de données.")
        return self.cancelled()

    def tournament_full(self):
        print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")

    def add_another_player(self):
        answer = input("Voulez-vous ajouter un autre joueur ? (Y / N) ")
        if answer.upper() == "Y":
            return True
        elif answer.upper() == "N":
            return False
        else:
            self.notify_invalid_choice()
            return False
