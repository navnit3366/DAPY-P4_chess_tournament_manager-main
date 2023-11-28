from tinydb import TinyDB
DATABASE_PATH = "./tournament_manager_database.json"


class Database:

    def __init__(self):
        self.database = TinyDB(DATABASE_PATH)
        self.current_tournament = None
        self.players_table = self.database.table("players")
        self.tournaments_table = self.database.table("tournaments")

    def get_db_object(self, object_id, table):
        """Retrieve an objet, using its id """
        return self.database.table(table).get(doc_id=int(object_id))

    def add_to_database(self, table_name, serialized_object):
        """Add an new object to the database.
        Arguments:
            - (str) Table name
            - (dictionary) serialized_object
        Returns:
            - (int) id of the newly added element."""
        table = self.database.table(table_name)
        table.insert(vars(serialized_object))
        doc_id = int(table.all()[-1].doc_id)
        return doc_id

    def empty_database_table(self, table_name):
        table = self.table(table_name)
        table.truncate()

    # TODO ajouter une fonction qui vérifie tous les éléments de la base de données
