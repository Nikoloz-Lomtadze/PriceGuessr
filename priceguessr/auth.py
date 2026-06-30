from priceguessr.models import Users
## კოდი აუტემფიკაციის log in  Sign up

class AuthManager:
    def __init__(self, database): # ბაზის ობიექტი
        self.database = database

    def signup(self, username, password): #Sign up
        conn = self.database.connect()
        try:  # ამატებს ახალ მომხმარებელს
            cursor = conn.cursor()
            prompt = """
            INSERT INTO users (username, password) VALUES (?, ?)
            """
            cursor.execute(prompt, (username, password))
            conn.commit()
            return Users(cursor.lastrowid, username) # გვიბრუნებს მომხმარებლის ობიექტს id,usernmae
            # lastrowid ახლად დამატებული row-ს  აიდი
        finally:
            conn.close()

    def login(self, username, password): #login
        conn = self.database.connect()
        try:
            cursor = conn.cursor()
            #ვეძებთ ცხრილში რომ მომხმარებელი და პაროლი ერთი იყოს
            prompt = """    
            SELECT * FROM users
            WHERE username = ? AND password = ?
            """ 
            cursor.execute(prompt, (username, password))
            row = cursor.fetchone() #
        finally:
            conn.close()

        if row is None:
            return None
        return Users(row["id"], row["username"]) # აქაც ვაბრუნებთ აიდის და მომხმარებელს
