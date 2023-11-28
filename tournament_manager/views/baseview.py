class BaseView():
    @staticmethod
    def render():
        print("")

    def get_user_choice(self):
        return input('\nQue souhaitez-vous faire ? ').lower()

    def notify_invalid_choice(self):
        print("Choix non valable !")

    def get_tournament_id(self):
        try:
            return int(input("Id d\'un tournoi existant ? "))
        except ValueError:
            print("L'id doit être un entier positif.")
            return self.get_tournament_id()

    @staticmethod
    def print_header(title):
        bars = "|==========" + "=" * len(title) + "==========|"
        print(
            f"\n{bars}\n"
            f"|          {title}          |\n"
            f"{bars}"
        )

    def alert_user(self, alert_text):
        print(alert_text)

    def print_player_details(self, unserialized_players_list, score=False):
        """Prints a list of players."""
        header = "Id\tPrénom\t\tNom\t\tSexe\t\tDate de naissance\tClassement\t"
        if score:
            header += "Score"
        print(header)
        if unserialized_players_list == []:
            print("- Aucun joueur à afficher -")
        else:
            for player in unserialized_players_list:
                player_line = f'{player.doc_id}\t{player["first_name"]}\t'
                if len(player["first_name"]) < 8:
                    player_line += '\t'
                player_line += f' {player["last_name"]}\t'
                if len(player["last_name"]) < 7:
                    player_line += '\t'
                player_line += f' {player["gender"]}\t\t {player["birth_date"]}\t\t {player["ranking"]}\t\t'
                if score:
                    player_line += f'{player["score"]}'
                print(player_line)

    def press_enter(self):
        input("Retour au menu de sélection.")

    def id_not_found(self, id, table_name):
        print(f"Id {id} introuvable dans la table \"{table_name}\".")

    def cancelled(self):
        return input("Opération annulée. Retour au menu de sélection.")

    def print_tournament_details_header(self):
        print(
            "Nom\t\t\t\t"
            "Lieu\t\t"
            "Date de début\t"
            "Date de fin\t"
            "Time control\t"
            "Tour joués"
        )

    def get_sorting_parameter(self, score):
        print(
            "1. Par nom de famille\n"
            "2. Par classement"
        )
        if score:
            print("3. Par score")
        return self.get_user_choice()

    @staticmethod
    def get_player_id():
        return input("Id du joueur : ")

    def print_tournament_details(self, tournament_details):
        """Prints tournament details."""
        tournament_line = f"{tournament_details['name']}"
        while len(tournament_line) < 32:
            tournament_line += " "
        tournament_line += f"{tournament_details['location']}\t"
        while len(tournament_line) < 46:
            tournament_line += " "
        tournament_line += f"{tournament_details['date_start']}\t"
        tournament_line += f"{tournament_details['date_end']}\t"
        tournament_line += f"{tournament_details['time_control']}\t\t"
        tournament_line += f"{len(tournament_details['rounds'])}\t"
        print(tournament_line)

    def type_error(self, type):
        print(f"Doit être de type {type}.")
