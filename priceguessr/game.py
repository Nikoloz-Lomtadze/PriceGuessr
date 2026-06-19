from priceguessr.models import Gameround,gameresult,GameSession
class GameManager:
    def __init__(self,database,item_provider):
        self.database = database
        self.item_provider = item_provider
        self.round_per_game = 10
    def start_game(self,user_id,mode,category = None):
        rounds = []
        for i in range(1,self.round_per_game+1):
            left_item,right_item = self.item_provider.get_two_items(category)
            Game_round = Gameround(i,left_item,right_item)
            rounds.append(Game_round)
        session = GameSession(user_id,mode,rounds)
        return session
    def submit_guess(self,session,chosen_item):
        if session.is_finished():
            raise ValueError("game is finished")
        current_round = session.get_current_round()
        if current_round.left_item.price > current_round.right_item.price:
            correct_item = current_round.left_item
        else:
            correct_item = current_round.right_item
        correct = correct_item.id == chosen_item.id
        if correct:
            points = 10
            session.score += points
            session.rounds_won += 1
        else:
            points = 0
        result = gameresult(
            current_round.round_number,
            correct,
            points,
            current_round.right_item,
            current_round.left_item,
            chosen_item,
            correct_item,
        )
        session.round_results.append(result)
        session.current_round +=1
        if session.is_finished():
            self.save_game(session)

        return result
    def save_game(self,session):
        rounds_played = len(session.rounds)
        if session.rounds_won > rounds_played/2:
            won = 1
        else:
            won = 0
        conn = self.database.connect()
        cursor = conn.cursor()
        prompt1 = """
        INSERT INTO games (user_id,mode,rounds_played,rounds_won,won,points) VALUES (?,?,?,?,?,?)
        """
        cursor.execute(prompt1,(session.user_id,session.mode.value,rounds_played,session.rounds_won,won,session.score))
        game_id = cursor.lastrowid
        prompt2 = """
        INSERT INTO game_rounds (game_id,round_number,left_item_name,right_item_name,chosen_item_name,correct_item_name,category_guessed,won,points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for i in session.round_results:
            cursor.execute(prompt2,(
                game_id,
                i.round_number,
                i.left_item.name,
                i.right_item.name,
                i.chosen_item.name,
                i.correct_item.name,
                i.chosen_item.category,
                 1 if i.correct else 0,
                i.points_earned
            ))
        conn.commit()
        conn.close()