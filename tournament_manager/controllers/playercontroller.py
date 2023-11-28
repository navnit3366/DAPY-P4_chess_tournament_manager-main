import re
from datetime import date

from tinydb import Query

from tournament_manager.views import PlayerHomeView
from ..models import Database, Player


class PlayerMenuController:
    """Controller for Player menu."""
    def __init__(self):
        self.view = PlayerHomeView()
        self.database = Database()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            # Lists all players in database
            all_players = self.database.players_table.all()
            list_players(self, all_players)
            self.view.press_enter()
            return self.run()
        elif next_action == '2':

            first_name = self.get_valid_first_name()
            last_name = self.get_valid_last_name()
            list_of_matches = self.find_player_by_name(first_name, last_name)
            if len(list_of_matches) != 0:
                self.view.print_player_details(list_of_matches)
            else:
                self.view.alert_user("Aucune correspondance dans la base de données.")

            self.view.press_enter()
            return self.run()
        elif next_action == '3':
            # Create new player and add them to the database
            new_player = self.create_new_player()
            if new_player is not None:
                new_player_id = self.database.add_to_database("players", new_player)
                self.view.alert_user(
                    f'---\n{new_player.first_name} {new_player.last_name} succesfully added with id {new_player_id}.'
                )
            self.view.press_enter
            return self.run()
        elif next_action == "4":
            self.update_player_infos()
            return self.run()
        elif next_action == "0":
            return "home"
        elif next_action == "9":
            return None
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def get_new_player_info(self):
        """Collects player info from the user."""
        self.view.print_adding_new_player()
        # Collecting player info
        first_name = self.get_valid_first_name()
        last_name = self.get_valid_last_name()
        if first_name is None or last_name is None:
            self.view.cancelled()
            return None
        birth_date = self.get_valid_birth_date()
        gender = self.get_valid_gender()
        ranking = self.get_valid_ranking()
        return [first_name, last_name, str(birth_date), gender, ranking]

    def get_valid_first_name(self):
        """Get valid first_name from user.
        Args:
            - None
        Returns:
            - a validated string."""
        pattern = r"\w+[-]?\w+"
        inputted_name = self.view.get_first_name()
        if inputted_name == "":
            return None
        elif re.fullmatch(pattern, inputted_name):
            return inputted_name
        else:
            self.view.alert_user("Le prénom doit être uniquement constitué de lettres (ou '-').")
            return self.get_valid_first_name()

    def get_valid_last_name(self):
        """Get valid last_name from user.
        Args:
            - None
        Returns:
            - a validated string."""
        pattern = r'[A-Za-z(\s)]*'
        inputted_name = self.view.get_last_name()
        if inputted_name == "":
            return None
        elif re.fullmatch(pattern, inputted_name):
            return inputted_name
        else:
            self.view.alert_user("Le nom de famille doit être uniquement constitué de lettres.")
            return self.get_valid_last_name()

    def get_valid_gender(self):
        inputted_gender = self.view.get_gender()
        if inputted_gender.upper() in ['F', 'M', 'X']:
            return inputted_gender
        else:
            self.view.alert_user("Le genre doit être 'F', 'M' or 'X'.")
            return self.get_valid_gender()

    def get_valid_birth_date(self):
        inputted_date = self.view.get_birth_date()
        listed_input = inputted_date.split("/")
        try:
            formatted_date = date(int(listed_input[2]), int(listed_input[1]), int(listed_input[0]))
            # format the French way
            formatted_date_fr = formatted_date.strftime('%d/%m/%Y')
            return formatted_date_fr
        except IndexError:
            self.view.alert_user("La date de nasisance doit être au format JJ-MM-AAAA.")
            return self.get_valid_birth_date()
        except ValueError:
            self.view.alert_user("La date de nasisance doit être au format JJ-MM-AAAA.")
            return self.get_valid_birth_date()

    def get_valid_ranking(self):
        """Prompt user for player ranking and validate data.
        Returns:
            - An integer, for player ranking."""
        inputted_ranking = self.view.get_ranking()
        try:
            return int(inputted_ranking)
        except ValueError:
            self.view.type_error("integer")
            return self.get_valid_ranking()

    def find_player_by_name(self, first_name, last_name):
        players_table = self.database.players_table
        return players_table.search((Query().first_name == first_name) & (Query().last_name == last_name))

    def create_new_player(self):
        """Add a player to the database.
        Returns:
            - A new instance of Player class
        """
        new_player_data = self.get_new_player_info()
        if new_player_data is None:
            return None
        existing_duplicate = self.find_player_by_name(new_player_data[0], new_player_data[1])
        # TODO transformer en une fonction search_player() qui servira aussi à aller update les infos du player
        if existing_duplicate != []:
            self.view.print_duplicate_alert(new_player_data, existing_duplicate)
            next_action = self.view.get_user_choice()
            if next_action == '1':
                self.update_player_infos()
            elif next_action == "2":
                return Player(*new_player_data)
            elif next_action == "3":
                self.view.cancelled()
            else:
                self.view.notify_invalid_choice()
        else:
            return Player(*new_player_data)

    def update_player_infos(self, player_id="", first_name="", last_name="", gender="", birth_date="", ranking=""):
        """Update a player in the database."""
        player_id = get_valid_player_id(self)
        existing_player = self.database.get_db_object(player_id, "players")

        self.view.print_player_details([existing_player])

        next_action = self.view.get_player_field_to_modify()
        # TODO convert to dictionary
        if next_action == "1":
            updated_field = "first_name"
        elif next_action == "2":
            updated_field = "last_name"
        elif next_action == "3":
            updated_field = "birth_date"
        elif next_action == "4":
            updated_field = "gender"
        elif next_action == "5":
            updated_field = "ranking"
        elif next_action == "0":
            self.view.cancelled()
            return None
        else:
            self.view.notify_invalid_choice()
            return None

        updated_info = self.view.get_updated_info()
        self.database.players_table.update({updated_field: updated_info}, doc_ids=[player_id])
        return None


# Had to put outside class to allow call from playercontroller
def list_players(self, players_list, score=False):
    """Lists players."""
    sorting_parameter = self.view.get_sorting_parameter(score)
    if sorting_parameter == "1":
        sorted_list = sorted(players_list, key=lambda x: x['last_name'])
    elif sorting_parameter == "2":
        sorted_list = sorted(players_list, key=lambda x: x['ranking'], reverse=True)
    elif sorting_parameter == "3" and score is True:
        sorted_list = sorted(players_list, key=lambda x: x['score'], reverse=True)
    else:
        self.view.notify_invalid_choice()
        return None

    self.view.print_player_details(sorted_list, score)
    return None


# Had to put outside class to allow call from playercontroller
def get_valid_player_id(self):
    inputted_id = self.view.get_player_id()
    try:
        return int(inputted_id)
    except ValueError:
        self.view.type_error("integer")
        return get_valid_player_id(self)
