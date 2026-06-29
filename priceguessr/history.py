# ეს კოდი უნდა გამოვიყენოთ რათა გამოვიყენოთ შემდეგ თამაშის ისტორიების სანახავად

from priceguessr.models import Matchrecord
class MatchHistory:
    def __init__(self,database): # ბაზის ობიექტი
        self.database = database
    def get_last_matches(self,user_id):
        conn = self.database.connect() # კავშირი ბაზასთან
        cursor = conn.cursor()
        prompt = """Select * FROM games where user_id = ? order by played_at DESC Limit 10""" # 10 ბოლო თამაშის ამოღება
        cursor.execute(prompt, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        matches = []
        for i in rows: # ვიღებთ ამოღებულ მონაცემებს და ვავსებთ ლისტს
            match = Matchrecord(
                i["id"],
                i["mode"],
                i["rounds_played"],
                i["rounds_won"],
                i["won"],
                i["played_at"],
                i["points"]
            )
            matches.append(match)
        return matches
        

