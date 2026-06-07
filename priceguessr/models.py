from enum import Enum
## here we collect main  values needed for out project, we save them during the game and will use them later
## we can use only these 3 modes, they are fixed 
class Gamemodes(str,Enum): ## str makes enum values behave like strings, useful for SQLite and comparisons
    Singleplayer = 'singleplayer'
    Multiplayer = 'multiplayer'
    vsbot = 'vsbot'
class Users:
    def __init__(self,user_id,username):
        self.user_id = user_id
        self.username = username
class Items:
    def __init__(self,Item_id,name,price,category,image_url):
        self.id = Item_id
        self.name = name
        self.price = price
        self.category = category
        self.image_url = image_url
class Gameround:
    def __init__(self,round_number,left_item,right_item):
        self.round_number = round_number
        self.left_item = left_item
        self.right_item = right_item
class GameSession:
    def __init__(self,user_id,mode,rounds):
        self.user_id = user_id
        self.mode = mode
        self.rounds = rounds
        self.current_round = 0
        self.score = 0
        self.rounds_won = 0
        self.round_results = []
    def get_current_round(self):
        return self.rounds[self.current_round]
    def is_finished(self):
        return self.current_round >= len(self.rounds)
class gameresult:
    def __init__(self,round_number,correct,points_earned,right_item,left_item,chosen_item,correct_item):
        self.round_number = round_number
        self.correct = correct
        self.points_earned = points_earned
        self.right_item = right_item
        self.left_item = left_item
        self.chosen_item = chosen_item
        self.correct_item = correct_item
class Matchrecord:
    def __init__(self,match_id,mode,rounds_played,rounds_won,won,played_at,points_count):
        self.match_id = match_id
        self.mode = mode
        self.rounds_played = rounds_played
        self.rounds_won = rounds_won
        self.won = won
        self.played_at = played_at
        self.points_count = points_count