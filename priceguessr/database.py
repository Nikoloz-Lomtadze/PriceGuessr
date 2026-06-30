## ეს ფაილი არის დატაბეიზისთან დასაკავშირებლად,ყველა თეიბლების შესაქმნელად
import sqlite3


class Database:
    def __init__(self, dbname): #ინიციალიზაციის დროს იქმნება თეიბლები

        self.dbname = dbname
        self.create_tables()

    def connect(self):  # დაკავშირების ფუნქცია
        connection = sqlite3.connect(self.dbname) # დავკავშირდეთ ბაზასთან
        connection.row_factory = sqlite3.Row # წვდომა query-ში სვეტებით


        connection.execute("PRAGMA foreign_keys = ON")
        #ამის მეშვეობით იგნორდება ის მონაცემები რომლებთაც არ აქვთ ვალიდური foreign key
        #მეორე მონაცემი
        return connection

    def create_tables(self): # თეიბლების შექმნის ფუნქცია
        conn = self.connect()
        cursor = conn.cursor()


        ## მომხმარებლის თეიბლი
        users_table = """

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )

        """


        #თეიბლი თამაშების რომლებიც ვითამაშეთ
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
        )

        """
        # თითოეული რაუნდის თეიბლები
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
        )

        """
        
        # ბოტის თეიბლის მონაცემები
        bot_table = """

        CREATE TABLE IF NOT EXISTS bot_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL UNIQUE,
            bot_score INTEGER NOT NULL,
            bot_rounds_won INTEGER NOT NULL,
            winner TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games(id)
        )

        """
        # მულტიპლეიერის თეიბლი
        multiplayer_table = """

        CREATE TABLE IF NOT EXISTS multiplayer_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_one_game_id INTEGER NOT NULL,
            player_two_game_id INTEGER NOT NULL,
            winner_user_id INTEGER,
            FOREIGN KEY (player_one_game_id) REFERENCES games(id),
            FOREIGN KEY (player_two_game_id) REFERENCES games(id),
            FOREIGN KEY (winner_user_id) REFERENCES users(id)
        )

        """
        # for loop-ით შევქმენით ყველა ცხრილი და გავუშვით ცვლილებები
        for table in [users_table, games_table, rounds_table,bot_table, multiplayer_table]:
            cursor.execute(table)

            
        conn.commit()
        conn.close()
