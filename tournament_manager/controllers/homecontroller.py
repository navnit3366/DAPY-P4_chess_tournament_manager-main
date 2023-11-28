from datetime import date

from tinydb import Query

from tournament_manager.views import HomeView
from ..models import Tournament, Database, TIME_CONTROL_TYPE


class HomeController:
    """Controller for Home menu."""
    def __init__(self):
        self.view = HomeView()
        self.database = Database()

    def run(self):
        """Run controller."""
        self.view.render()

        next_action = self.view.get_user_choice()
        if next_action == "1":
            # Displays all tournaments
            self.show_tournaments_details()
            self.view.press_enter()
            return self.run()
        elif next_action == "2":
            # Creation of a new tournament
            new_tournament_infos = self.get_new_tournament_info()
            if new_tournament_infos is not None:
                new_tournament = Tournament(*new_tournament_infos)
                self.add_new_tournament_to_database(new_tournament)
            return self.run()
        elif next_action == "3":
            return "tournament_menu"
        elif next_action == '4':
            return "players_menu"
        elif next_action == "9":
            return None
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def show_tournaments_details(self):
        tournaments_list = self.database.tournaments_table.all()
        self.view.print_tournament_details_header()
        if len(tournaments_list) == 0:
            self.view.alert_user("Aucun tournoi à afficher.")
        else:
            for tournament in tournaments_list:
                self.view.print_tournament_details(tournament)
        return None

    def get_new_tournament_info(self):
        """Get all infos to create a new tournament object.
        Args:
            - None
        Returns:
            - A list containing collected data"""
        # TODO récupérer la liste des champs avec "signature(Tournament)" ?
        name = self.get_valid_tournament_name()
        if name is None:
            return None
        else:
            location = self.get_valid_location()
            date_beginning = self.get_valid_date("start")
            date_ending = self.get_valid_date("end")
            # TODO check end_date is after beginning date
            time_control = self.get_valid_time_control()
            description = self.view.get_description()
            return [name, location, date_beginning, date_ending, [], {}, time_control, description]

    def get_valid_tournament_name(self):
        """Get an unique tournament name."""
        name = self.view.get_name()
        existing_tournament = self.database.tournaments_table.search(Query().name == name)
        if len(existing_tournament) == 0:
            return name
        else:
            tournament_id = existing_tournament[0].doc_id
            self.view.alert_user(f"Un tournoi porte déjà ce nom dans la base de données (id = {tournament_id})")
            self.view.cancelled()
            return None

    def get_valid_location(self):
        return self.view.get_location()

    def get_valid_date(self, date_type):
        if date_type == "start":
            inputted_date = self.view.get_start_date()
        elif date_type == "end":
            inputted_date = self.view.get_end_date()
        elif date_type == "birth":
            inputted_date = self.view.get_birth_date()

        split_date = inputted_date.split("/")
        try:
            formatted_date = date(int(split_date[2]), int(split_date[1]), int(split_date[0]))
            # format the French way
            formatted_date_fr = formatted_date.strftime('%d/%m/%Y')
        except IndexError:
            self.view.alert_user("La date de naissance doit être au format JJ/MM/AAAA (mauvais format).")
            return self.get_valid_date(date_type)
        except ValueError:
            self.view.alert_user("La date de naissance doit être au format JJ/MM/AAAA (date impossible).")
            return self.get_valid_date(date_type)

        return formatted_date_fr

    def get_valid_time_control(self):
        time_control = self.view.get_time_control()
        if time_control in TIME_CONTROL_TYPE:
            return time_control
        else:
            self.view.alert_user("Time control doit être \"bullet\" ou \"blitz\" ou \"rapide\"")
            self.get_valid_time_control()

    def add_new_tournament_to_database(self, tournament):
        """Add a new tournament to the database.
        Args:
            - Informations of new tournament
        Returns:
            - database id of the new tournament"""
        table_name = "tournaments"
        tournament_id = self.database.add_to_database(table_name, tournament)
        alert = f'---\n{tournament.name} ajouté.e à la base de données avec l\'id {tournament_id}.'
        self.view.alert_user(alert)
        return None
