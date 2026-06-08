from priceguessr.models import Matchrecord
class MatchHistory:
    def __init__(self,database):
        self.database = database
    def get_last_matches(self,user_id):
        conn = self.database.connect()
        cursor = conn.cursor()
        prompt = """Select * FROM games where user_id = ? order by played_at DESC Limit 10"""
        cursor.execute(prompt,user_id)
        rows = cursor.fetchall()
        conn.close()
        matches = []
        for i in rows:
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
        

