from priceguessr.models import Gameround, gameresult, GameSession


class GameManager:
    def __init__(self, database, item_provider):

        self.database = database
        self.item_provider = item_provider
        self.round_per_game = 10

    def create_rounds(self, category=None): ## creating list of items (20pcs)
        rounds = []

        for round_number in range(1, self.round_per_game + 1):
            left_item, right_item = self.item_provider.get_two_items(category)
            rounds.append(Gameround(round_number, left_item, right_item))

        return rounds

    def start_game(self, user_id, mode, category=None):  # starting the game
        return GameSession(user_id, mode, self.create_rounds(category))

    def get_correct_item(self, game_round): ## checking which item is more expensive
        
        if game_round.left_item.price > game_round.right_item.price:
            return game_round.left_item
        
        return game_round.right_item

    def create_result(self, game_round, chosen_item):

        if chosen_item.id not in [game_round.left_item.id, game_round.right_item.id]:
            raise ValueError("chosen item is not part of this round")

        correct_item = self.get_correct_item(game_round) ## check which item is correct
        correct = correct_item.id == chosen_item.id ## its true or false 
        points = 10 if correct else 0 

        return gameresult( ## returning result of the round
            game_round.round_number,
            correct, ## true or false
            points, # 0 or 10
            game_round.right_item, 
            game_round.left_item,
            chosen_item, # chosen item
            correct_item # which one is correct
        )

    def submit_guess(self, session, chosen_item): ## ვცვლით სესიის მონაცემებს

        if session.is_finished(): #cant submit if game is finished
            raise ValueError("game is finished")

        result = self.create_result(session.get_current_round(), chosen_item)
        session.score += result.points_earned

        if result.correct:
            session.rounds_won += 1

        session.round_results.append(result)
        session.current_round += 1

        if session.is_finished():
            self.save_game(session)

        return result

    def save_game(self, session, won_override=None):
        rounds_played = len(session.rounds)
        if won_override is None:
            won = 1 if session.rounds_won > rounds_played / 2 else 0 # აქ არის ის პირობა თუ რატო უნდა ჩაითვალოს თამაში მოგებული
        else:
            won = won_override

        conn = self.database.connect()
        cursor = conn.cursor()

        cursor.execute( ## შევავასოთ ბაზა ახალი თამაშის მონაცემებით
            """
            INSERT INTO games(user_id, mode, rounds_played, rounds_won, won, points) VALUES (?, ?, ?, ?, ?, ?)
            """,(
                session.user_id,
                session.mode.value,
                rounds_played,
                session.rounds_won,
                won,
                session.score
                )
                    )
        game_id = cursor.lastrowid

        for result in session.round_results:
            cursor.execute( ## შევავსოთ რაუნდების მონაცემები
                """
                INSERT INTO game_rounds (game_id, round_number, left_item_name, right_item_name,chosen_item_name, correct_item_name, category_guessed,won, points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,(
                    game_id,
                    result.round_number,
                    result.left_item.name,
                    result.right_item.name,
                    result.chosen_item.name,
                    result.correct_item.name,
                    result.chosen_item.category,
                    1 if result.correct else 0,
                    result.points_earned
                    )
                         )

        conn.commit()
        conn.close()
        return game_id
