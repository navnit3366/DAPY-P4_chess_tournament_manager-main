import random
from datetime import datetime

from tinydb import Query

from ..views.tournamentmenuview import TournamentHomeView
from ..models import Player, Tournament, Round, Match, Database
from ..models import PLAYERS_PER_TOURNAMENT, MAX_ROUNDS, SCORE_VICTORY, SCORE_DEFEAT, SCORE_DRAW
from .playercontroller import list_players, get_valid_player_id


class TournamentMenuController:
    """Controller for Tournament menu."""
    def __init__(self):
        self.view = TournamentHomeView()
        self.current_tournament = None
        self.database = Database()

    def run(self):
        self.view.render(self.current_tournament)
        next_action = self.view.get_user_choice()

        if next_action in ["2", "3", "4", "5", "6", "7"]:
            # if a current_tournament is needed but none is currently selected
            if self.current_tournament is None:
                selected_tournament = self.get_current_tournament()
                if selected_tournament is not None:
                    self.current_tournament = selected_tournament
                else:
                    self.view.cancelled()
                    return self.run()

        if next_action == "1":
            # Change selected tournament
            self.current_tournament = self.get_current_tournament()
            return self.run()
        if next_action == "2":
            # Selected add players to tournament
            if len(self.current_tournament.players) >= PLAYERS_PER_TOURNAMENT:
                self.view.tournament_full()
                self.view.cancelled()
            else:
                add_another = True
                while add_another and len(self.current_tournament.players) < PLAYERS_PER_TOURNAMENT:
                    player_id = get_valid_player_id(self)
                    self.add_player_to_tournament(player_id)
                    add_another = self.view.add_another_player()

                if len(self.current_tournament.players) == PLAYERS_PER_TOURNAMENT:
                    # notifies if it was the last player
                    self.view.alert_user("8ème participant.e ajouté.e au tournoi. Le tournoi est désormais plein ! ")

                self.view.press_enter()
            return self.run()
        elif next_action == "3":
            # Selected "New round"

            # TODO create two exceptions for ReachedMaxRound and UnfinishedLastRound
            if self.check_ready_for_new_round():
                new_round = self.create_new_round()
                self.current_tournament.rounds.append(new_round)
                self.update_rounds_in_database()
            else:
                self.view.cant_start_round()

            self.view.press_enter()
            return self.run()
        elif next_action == "4":
            # Updatting round's results

            # TODO check if last round is finished.
            round_to_update = self.current_tournament.rounds[-1]
            for match_to_update in round_to_update.matchs:
                # print(match_to_update)
                self.view.alert_user(f"Updating match {match_to_update[0][0]} contre {match_to_update[1][0]}")
                match_index = round_to_update.matchs.index(match_to_update)

                new_match = self.get_updated_match(match_to_update)
                self.current_tournament.rounds[-1].matchs[match_index] = new_match
                self.current_tournament.rounds[-1].end_datetime = str(datetime.today())

                # Updating players scores
                self.current_tournament.players[str(new_match[0][0])] += new_match[0][1]
                self.current_tournament.players[str(new_match[1][0])] += new_match[1][1]

            self.view.print_round_ended(self.current_tournament.rounds[-1])
            # Updating database
            self.update_rounds_in_database()
            self.update_players_in_database()

            self.view.press_enter()
            return self.run()
        elif next_action == "5":
            # Browse and print entrants infos
            entrants_list = []
            for player_id in self.current_tournament.players.keys():
                entrant_infos = self.database.get_db_object(int(player_id), "players")
                entrant_infos["score"] = self.current_tournament.players[str(player_id)]
                entrants_list.append(entrant_infos)

            list_players(self, entrants_list, score=True)
            self.view.press_enter()
            return self.run()
        elif next_action == "6":
            # Selected "prints rounds"
            self.show_rounds_details()

            self.view.press_enter()
            return self.run()
        elif next_action == "7":
            # List matches
            self.view.print_match_header()
            for round in self.current_tournament.rounds:
                print(round.name)
                for match in round.matchs:
                    self.view.print_match_details(match)

            self.view.press_enter()
            return self.run()
        elif next_action == "0":
            return "home"
        elif next_action == "9":
            return None
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def show_rounds_details(self):
        if len(self.current_tournament.rounds) > 0:
            self.view.print_round_header()
            for round in self.current_tournament.rounds:
                self.view.print_round_details(round)
        else:
            self.view.alert_user("Aucun round à afficher.")

    def update_players_in_database(self):
        """Update players dictionary in the database"""
        # self.view.alert_user(self.current_tournament.players)
        name = self.current_tournament.name
        self.database.tournaments_table.update({"players": self.current_tournament.players}, Query().name == name)

    def update_rounds_in_database(self):
        serialized_rounds = [round.serialize() for round in self.current_tournament.rounds]
        name = self.current_tournament.name
        self.database.tournaments_table.update({"rounds": serialized_rounds}, Query().name == name)

    def get_current_tournament(self):
        """Prompts user to select a tournament as current tournament.
        Returns:
            - an tournament object (unserialized) or None if """
        tournaments_table = self.database.tournaments_table
        if len(tournaments_table.all()) == 0:
            self.view.no_tournament_in_database()
            return None

        # Trying to fetch tournament
        try:
            inputted_id = self.view.get_tournament_id()
            serialized_tournament = tournaments_table.get(doc_id=inputted_id)
        except AttributeError:
            self.view.id_not_found(inputted_id, "tournaments")
            return None

        tournament = self.unserialize_object(serialized_tournament, type="tournaments")
        name = tournament.name
        self.view.alert_user(f"Tournoi '{name}' sélectionné comme tournoi en cours.")
        return tournament

    def add_player_to_tournament(self, player_id):
        """ Add a player to tournament, using their id. """
        # Check if player is not already registered in tournament
        if len(self.current_tournament.players) > 0:
            if str(player_id) in self.current_tournament.players.keys():
                self.view.alert_user("Player already in tournament.")
                return None

        # Making sure que le player est bien dans la DB
        db_match = self.database.players_table.get(doc_id=player_id)
        if db_match is not None:
            self.current_tournament.players[str(player_id)] = 0
            self.update_players_in_database()
            self.view.alert_user(f"Joueur {player_id} ajouté.")
        else:
            self.view.id_not_found(player_id, "players")

    def create_new_round(self):
        """Creates a new round for current tournament."""
        round_number = int(len(self.current_tournament.rounds))+1

        if round_number == 1:
            # first round, players order is based on ranking
            # and 1 meets 4, 2 meets 5, etc
            players_order = self.sort_players(self.current_tournament.players, by='ranking')
        else:
            players_order = self.sort_players(self.current_tournament.players, by='score')

        paired_players = self.pair_players(players_order, round_number)

        new_round_matchs = []
        for pair in paired_players:
            reverse = random.randint(0, 1)
            if not reverse:
                new_match = Match(([pair[0], "-"], [pair[1], "-"]))
            else:
                new_match = Match(([pair[1], "-"], [pair[0], "-"]))
            new_round_matchs.append(new_match)

        # New round infos
        round_name = f'Round {round_number}'
        round_starttime = str(datetime.today())
        round_endtime = None

        new_round = Round(round_name, round_starttime, round_endtime, new_round_matchs)
        self.view.alert_user(f'{new_round.name} créé le {new_round.start_datetime}.')
        for match in new_round.matchs:
            p1 = match[0][0]
            p2 = match[1][0]
            self.view.alert_user(f'{p1} joue les noirs, {p2} joue les blancs. Bon match !')
        return new_round

    def check_ready_for_new_round(self):

        if len(self.current_tournament.rounds) > 0:
            for match in self.current_tournament.rounds[-1].matchs:
                if match[0][1] == 0 and match[1][1] == 0:
                    return False

        if len(self.current_tournament.players) != PLAYERS_PER_TOURNAMENT:
            error_message = (
                "Le round ne peut pas commencer car le nombre de joueurs est incorrect."
                f"Actuellement {len(self.current_tournament.players)} joueurs au lieu de {PLAYERS_PER_TOURNAMENT}.")
            self.view.alert_user(error_message)
            return False
        elif len(self.current_tournament.rounds) >= MAX_ROUNDS:
            self.view.print_reached_max_rounds(MAX_ROUNDS)
            return False
        else:
            return True

    def sort_players(self, entrants_list, by='score'):
        """ Sorts player to generate pairs according to the swiss tournament pattern.
        Args:
            - a list of players
            - by -- the parameter by which players will be sorted. Can be 'score' or 'ranking'
        Returns:
        - a sorted list of players' ids
        """

        # filters the database to only get this tournament's entrants
        infos = []
        for entrants_id in entrants_list.keys():
            # extract player infos from the database and add score
            players_infos = self.database.players_table.get(doc_id=int(entrants_id))
            players_infos["score"] = int(self.current_tournament.players[str(entrants_id)])
            infos.append(players_infos)

        if by == "ranking":
            return [player.doc_id for player in sorted(infos, key=lambda x:x['ranking'], reverse=True)]
        elif by == 'name':
            return [player.doc_id for player in sorted(infos, key=lambda x:x['last_name'])]
        elif by == 'score':
            return [player.doc_id for player in sorted(infos, key=lambda x: (x['score'], x['ranking']), reverse=True)]
        else:
            message = (f'Cannot sort by {by}. Please sort by \'score\', \'ranking\' or \'name\' instead.')
            self.view.alert_user(message)

    def pair_players(self, players_ordered_list, round_number):
        """Pairs players together from player list.
        Args:
            - An ordered list of players_ids
        Returns:
            - A list of this round's pairs """
        pair_list = []

        if round_number == 1:
            # Pairs weirdly : 1 with 5, 2 with 6, etc
            half = int(PLAYERS_PER_TOURNAMENT/2)
            # Making special pairs for first round
            highest_half = players_ordered_list[:half]
            lowest_half = players_ordered_list[half:]

            for position in range(len(highest_half)):
                duo = ([highest_half[position], lowest_half[position]])
                pair_list.append(duo)
        elif round_number > 1:
            # Pairs from top to bottom, avoiding matching players who already played together
            players_left_to_match = players_ordered_list
            while players_left_to_match != []:
                p1_id = players_left_to_match[0]
                p2_id = self.first_unmet_partner(p1_id, players_left_to_match[1:])
                duo = (p1_id, p2_id)
                pair_list.append(duo)
                players_left_to_match.remove(p1_id)
                players_left_to_match.remove(p2_id)

        return pair_list

    def first_unmet_partner(self, player_to_match, list_of_candidates):
        met_players = self.get_previously_met_players(player_to_match)
        # print(f"    Matching for {player_to_match}, who already met {met_players}")
        for candidate in list_of_candidates:
            if candidate not in met_players:
                return candidate

        # if we run out of candidates AKA player_to_match already met everyone
        return list_of_candidates[0]

    def get_previously_met_players(self, player_id):
        """Browse previous rounds to find past opponents.
        Arguments:
            - A player's id
        Returns:
            - A list of past opponents ids"""
        met_players = []
        for past_round in self.current_tournament.rounds:
            for past_match in past_round.matchs:
                if player_id == past_match[0][0]:
                    met_players.append(past_match[1][0])
                elif player_id == past_match[1][0]:
                    met_players.append(past_match[0][0])
                else:
                    pass
        return met_players

    def get_valid_score(self, player_id):
        inputted_score = self.view.get_match_score(player_id)
        if inputted_score in [SCORE_VICTORY, SCORE_DRAW, SCORE_DEFEAT]:
            return inputted_score
        else:
            self.view.alert_user(f'Le score doit être 0, 1 ou 0.5. Ne peut pas être {inputted_score}')
            return self.get_valid_score(player_id)

    def get_updated_match(self, match):
        p1_id = match[0][0]
        p2_id = match[1][0]
        score1 = self.get_valid_score(p1_id)
        score2 = self.get_valid_score(p2_id)
        if score1 + score2 == 1:
            new_match = Match(([p1_id, score1], [p2_id, score2]))
            return new_match
        else:
            return None

    def unserialize_object(self, serialized_object, type):
        try:
            if type.lower() == "players":
                object = Player(*serialized_object.values())
            elif type.lower() == "tournaments":
                object = Tournament(*serialized_object.values())
            else:
                error = f"Provided type '{type}'' is not a valid database table."
                raise error
            return object
        except AttributeError:
            error_message = "Object provided is not valid."
            self.view.alert_user(error_message)
            return None
