PLAYERS_PER_TOURNAMENT = 8
MAX_ROUNDS = 4
SCORE_VICTORY = 1.0
SCORE_DRAW = 0.5
SCORE_DEFEAT = 0.0

TIME_CONTROL_TYPE = [
    "bullet",
    "blitz",
    "fast"
]


class Tournament:
    """Un tournoi
    TODO Gestion du temps"""

    def __init__(self, name, location, date_start, date_end, rounds, players, time_control, description):
        self.name = name
        self.location = location
        self.date_start = date_start
        self.date_end = date_end
        self.rounds = [Round(
            round_info['name'],
            round_info['start_datetime'],
            round_info['end_datetime'],
            round_info['matchs']) for round_info in rounds]
        self.players = players
        self.time_control = time_control
        self.description = description

    def __str__(self):
        print(
            f"{self.name} (Tournament object)\n"
            f"{self.location}\n")

    def serialize(self):
        composition = vars(self)
        composition['rounds'] = [round for round in self.rounds]
        # composition['matchs'] = [str(match_) for match_ in self.matchs]
        return composition


class Round:
    """ Un tour de jeu. """

    def __init__(self, turn_name, start_datetime, end_datetime, matchs):
        """Initialize a round."""
        self.name = turn_name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.matchs = [Match(match) for match in matchs]

    def mark_as_finished(self, end_datetime):
        """Mark round as finished, sets endtime and calls for an update of match results."""
        self.end_datetime = end_datetime
        self.is_finished = True

        for match in self.matchs:
            match.update_results(1, 0)
        return True

    def serialize(self):
        composition = vars(self)
        composition['matchs'] = [match_ for match_ in self.matchs]
        return composition

    def __str__(self):
        return str(self.matchs)

    def __repr__(self):
        return self.__str__()


class Match(tuple):

    def serialize(self):
        print_duet = print(self)
        return print_duet
