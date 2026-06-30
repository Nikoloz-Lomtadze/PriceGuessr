from enum import Enum
#ჩვენ ამ ფაილში ვქმნით ობიექტებს თამაშისთვის
# str, Enum - ის მეშვეობით ჩვენ გვაქვს ფიქსირებული მონაცემები რომლებიც იქცევიან
# როგორც სტრინგები
class Gamemodes(str, Enum): # თამაშის მოდების ვარიანტები

    Singleplayer = "singleplayer"
    Multiplayer = "multiplayer"
    vsbot = "vsbot"
class Users: # იუსერის ობიექტი
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username


class Items: # ნივთების ობიექტები (პაროლი არაა აქ)
    def __init__(self, item_id, name, price, category, image_url):
        self.id = item_id
        self.name = name
        self.price = price
        self.category = category
        self.image_url = image_url


class Gameround: # თამაშის რაუნდის ობიექტი
    def __init__(self, round_number, left_item, right_item):
        self.round_number = round_number
        self.left_item = left_item
        self.right_item = right_item


class GameSession: # სესიის ობიექტი
    def __init__(self, user_id, mode, rounds):
        self.user_id = user_id
        self.mode = mode
        self.rounds = rounds
        self.current_round = 0
        self.score = 0
        self.rounds_won = 0
        self.round_results = []

    def get_current_round(self): # გვაძლევს მარცხენა და მარჯვენა ნივთს
        return self.rounds[self.current_round]

    def is_finished(self): # ამოწმებს მორჩა თუ არა თამაში
        return self.current_round >= len(self.rounds)


class gameresult: # ობექტი რაუნდის შედეგებზე
    def __init__(self, round_number, correct, points_earned, right_item,left_item, chosen_item, correct_item):
      
        self.round_number = round_number
        self.correct = correct
        self.points_earned = points_earned
        self.right_item = right_item
        self.left_item = left_item
        self.chosen_item = chosen_item
        self.correct_item = correct_item


class BotGameSession(GameSession): # ბოტის ობიექტი
    def __init__(self, user_id, rounds):
        super().__init__(user_id, Gamemodes.vsbot, rounds)
        self.bot_score = 0
        self.bot_rounds_won = 0


class BotRoundResult: # ბოტის შედეგი
    def __init__(self, user_result, bot_chosen_item, bot_correct,
                 bot_points, game_over, winner=None):
        self.user_result = user_result
        self.bot_chosen_item = bot_chosen_item
        self.bot_correct = bot_correct
        self.bot_points = bot_points
        self.game_over = game_over
        self.winner = winner


class MultiplayerGameSession(GameSession): #მულტიპლეიერის სესია
    def __init__(self, player_one_id, player_two_id, rounds):
        super().__init__(player_one_id, Gamemodes.Multiplayer, rounds)
        self.player_two_id = player_two_id
        self.player_two_score = 0
        self.player_two_rounds_won = 0
        self.player_two_results = []
        self.pending_guesses = {}


class MultiplayerRoundResult: # მულტიპლეიერის რაუნდის შედეგი
    def __init__(self, round_number, player_one_result, player_two_result,
                 game_over, winner=None):
        self.round_number = round_number
        self.player_one_result = player_one_result
        self.player_two_result = player_two_result
        self.game_over = game_over
        self.winner = winner


class Matchrecord: # შედეგის ობიექტი
    def __init__(self, match_id, mode, rounds_played, rounds_won, won,
                 played_at, points_count):
        self.match_id = match_id
        self.mode = mode
        self.rounds_played = rounds_played
        self.rounds_won = rounds_won
        self.won = won
        self.played_at = played_at
        self.points_count = points_count
