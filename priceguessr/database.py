import sqlite3
## creating tables for our need users,finished games,every round played
class Database:
    def __init__(self,dbname):
        self.dbname = dbname
        self.create_tables()
    def connect(self):
        connection = sqlite3.connect(self.dbname)
        connection.row_factory = sqlite3.Row
        return connection
    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        users_table = """
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )"""

        games_table = """
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mode TEXT NOT NULL,
                rounds_played INTEGER NOT NULL,
                rounds_won INTEGER NOT NULL,
                won INTEGER NOT NULL,
                points INTEGER NOT NULL,
                played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )"""
        rounds_table = """
            CREATE TABLE IF NOT EXISTS game_rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                round_number INTEGER NOT NULL,
                left_item_name TEXT NOT NULL,
                right_item_name TEXT NOT NULL,
                chosen_item_name TEXT NOT NULL,
                correct_item_name TEXT NOT NULL,
                category_guessed TEXT NOT NULL,
                won INTEGER NOT NULL,
                points INTEGER NOT NULL,
                FOREIGN KEY (game_id) REFERENCES games(id)
            )"""
        for i in [users_table,games_table,rounds_table]:
            cursor.execute(i)
        conn.commit()
        conn.close()