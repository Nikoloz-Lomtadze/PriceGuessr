from priceguessr.game import GameManager
from priceguessr.models import *


class MultiplayerManager:
    def __init__(self, database, item_provider):

        self.database = database
        self.game_manager = GameManager(database, item_provider) ## game manager ობიექტი

    def start_game(self, player_one_id, player_two_id, category=None): # თამაშის დაწყება
        
        if player_one_id == player_two_id:
            raise ValueError("multiplayer requires two different users") # უნდა იყოს ორი განსხვავებული მოთამაშე

        self.check_user_exists(player_one_id)
        self.check_user_exists(player_two_id)
        rounds = self.game_manager.create_rounds(category) #ვქმნით რაუნდების ლისტს (id,first item,second item)
        
        return MultiplayerGameSession(player_one_id, player_two_id, rounds) # იქმნება მულტიპლეიერის ობიექტი 

    def submit_guess(self, session, player_number, chosen_item):

        if session.is_finished():
            raise ValueError("game is finished") #თამაში არ უნდა იყოს დსრულებული
        
        if player_number not in [1, 2]:
            raise ValueError("player number must be 1 or 2") # მოთამაშე ან პირველია ან მეორე
        
        if player_number in session.pending_guesses: #ერთხელ უნდ ააირჩიო ერთ რაუნდში
            raise ValueError("this player already guessed in the current round")

        game_round = session.get_current_round() #იმ წამიერი რაუნდი
        
        if chosen_item.id not in [game_round.left_item.id, game_round.right_item.id]: #ვამოწმებთ ორიდან ერთი თუ ავირჩიეთ
            raise ValueError("chosen item is not part of this round")

        session.pending_guesses[player_number] = chosen_item # რა აირჩია მოთამაშემ

        if len(session.pending_guesses) < 2:
            return None

        player_one_result = self.game_manager.create_result(
            game_round,
            session.pending_guesses[1] # ვამოწმებთ 1 მოთამაშის არჩეული სწორია თუ არა
         )
        player_two_result = self.game_manager.create_result(
            game_round,  # მეორე მოთამაშის არჩეული თუ სწორია
            session.pending_guesses[2]
        )

        session.score += player_one_result.points_earned # ვამატებთ ქულებს
        if player_one_result.correct:
            session.rounds_won += 1 # ვამატებთ მოგებულ რაუნდებს

        session.player_two_score += player_two_result.points_earned # ვამატებთ ქულებს
        if player_two_result.correct:
            session.player_two_rounds_won += 1 # ვამატებთ მოგებულ რაუნდებს

        session.round_results.append(player_one_result)
        session.player_two_results.append(player_two_result)
        session.pending_guesses.clear()

        session.current_round += 1 # გადავდივართ შემდეგ რაუნდზე

        winner = None

        if session.is_finished():

            winner = self.get_winner(session)

            self.save_multiplayer_game(session, winner) # ვიმახსოვრებთ ვინ მოიგო და მონაცემებს

        return MultiplayerRoundResult(
            game_round.round_number,
            player_one_result,
            player_two_result,
            session.is_finished(),
            winner
        )

    def get_winner(self, session): # რომელმა მოთამაშემ მოიგო თამაში მთლიანობაში
        if session.score > session.player_two_score:
            return 1
        if session.player_two_score > session.score:
            return 2
        return 0

    def save_multiplayer_game(self, session, winner): # ვიმახსოვრებთ მონაცემებს
        player_one_won = 1 if winner == 1 else 0
        player_two_won = 1 if winner == 2 else 0

        player_one_game_id = self.game_manager.save_game(
            session,
            player_one_won
            )

        player_two_session = GameSession(
            session.player_two_id,
            Gamemodes.Multiplayer,
            session.rounds
        )

        player_two_session.current_round = len(session.rounds)
        player_two_session.score = session.player_two_score
        player_two_session.rounds_won = session.player_two_rounds_won
        player_two_session.round_results = session.player_two_results

        player_two_game_id = self.game_manager.save_game(
            player_two_session,
            player_two_won
        ) # ვიმახსოვრებთ მეორე მოთამაშის 

        if winner == 1:
            winner_user_id = session.user_id
        elif winner == 2:
            winner_user_id = session.player_two_id
        else:
            winner_user_id = None

        conn = self.database.connect()
        cursor = conn.cursor()
        # ვამატებთ ისტორიას ბაზაში
        cursor.execute(
            """
            INSERT INTO multiplayer_matches (player_one_game_id, player_two_game_id, winner_user_id)
            VALUES (?, ?, ?)
            """,
            (player_one_game_id, player_two_game_id, winner_user_id)
        )
        conn.commit()
        conn.close()

    def check_user_exists(self, user_id): # сhecking if user is real

        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        conn.close()

        if row is None:
            raise ValueError(f"user {user_id} does not exist")
