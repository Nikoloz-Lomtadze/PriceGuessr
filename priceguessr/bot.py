import random
from priceguessr.game import GameManager
from priceguessr.models import BotGameSession, BotRoundResult


class BotManager:
    def __init__(self, database, item_provider, accuracy=0.67): #აქ შეგვიძლია შევცვალოთ თუ რამდენად სწორად იცნობს ბოტი
        
        self.database = database
        self.game_manager = GameManager(database, item_provider) # gamemanager object
        self.accuracy = accuracy

    def start_game(self, user_id, category=None): # კატეგორია მერე ჩაეწერება
        rounds = self.game_manager.create_rounds(category) # რაუნდების ლისტი ნივთებით
        
        return BotGameSession(user_id, rounds) # ბოტის სესიის ობიექტი

    def submit_guess(self, session, chosen_item):
        if session.is_finished():
            raise ValueError("game is finished") # თამაში არ უნდა იყოს დასრულებული

        game_round = session.get_current_round() ## returning result of the round
        user_result = self.game_manager.create_result(game_round, chosen_item)
        correct_item = user_result.correct_item
        ## random.random აბრუნებს 0-1 floats
        if random.random() < self.accuracy: ## აქ ბოტი ირჩევს ნივთს
            bot_chosen_item = correct_item
        elif correct_item.id == game_round.left_item.id: # ირჩევს არასწორს
            bot_chosen_item = game_round.right_item
        else:
            bot_chosen_item = game_round.left_item 

        bot_correct = bot_chosen_item.id == correct_item.id #რეგისტრაცია იმის სწორია თუ არა და ქულების განსაზღვრა
        bot_points = 10 if bot_correct else 0
        session.score += user_result.points_earned # მოგებული რაუნდების დამატება
        
        if user_result.correct:
            session.rounds_won += 1

        session.bot_score += bot_points
        if bot_correct:
            session.bot_rounds_won += 1

        session.round_results.append(user_result)
        session.current_round += 1

        winner = None
        if session.is_finished(): #ვინ მოიგო საბოლოოდ და
            winner = self.get_winner(session)
            won = 1 if winner == "user" else 0
            game_id = self.game_manager.save_game(session, won)
            self.save_bot_result(game_id, session, winner)

        return BotRoundResult(
            user_result,
            bot_chosen_item,
            bot_correct,
            bot_points,
            session.is_finished(),
            winner
        )

    def get_winner(self, session):
        if session.score > session.bot_score:
            return "user"
        if session.bot_score > session.score:
            return "bot"
        return "tie"

    def save_bot_result(self, game_id, session, winner): # ბოტის მონაცემების დამატება
        conn = self.database.connect() 
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO bot_games (game_id, bot_score, bot_rounds_won, winner) VALUES (?, ?, ?, ?)
            """,(game_id, session.bot_score, session.bot_rounds_won, winner)
        )
        conn.commit()
        conn.close()
