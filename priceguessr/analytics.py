# ამ ფაილში არის კოდები რომლებსაც გამოვიყენებთ ანალიტიკისთვის

class Analytics:
    def __init__(self,database): # დატაბეიზის ობიექტი
        self.database = database

    def get_mode_stats(self,user_id):
        conn = self.database.connect() # ვაგებთ კავშირს
        cursor = conn.cursor() # კურსორი

        #  ვაჯგუფებთ mode-ბად და ვიგებთ მონაცემებს, რამდენი თამაში ვითამაშეთ, რამდენი მოვიგეთ
        # რამდენი ქულა გვაქ, საშუალო ქულა.
        prompt = """ 
        SELECT
        mode,
        COUNT(*) AS games_count,
        SUM(won) AS wins_count,
        SUM(points) AS total_points,
        AVG(points) AS average_points
        from games
        WHERE user_id = ?
        group by mode
        """
        cursor.execute(prompt,(user_id,)) # გავუშვათ ჩვენს იუზერზე
        rows = cursor.fetchall() # წამოღებული მონაცემები
        conn.close()

        # შევქმნათ ლისტი და შევავავსოთ დიქშიონერებით სადაც მონაცემებია
        stats = []
        for i in rows:
            variable = {
                'mode':i['mode'],
                'games_count':i['games_count'],
                'wins_count':i['wins_count'],
                'total_points':i['total_points'],
                'avarage_points':i['average_points']
            }
            stats.append(variable)
        return stats
