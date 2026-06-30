from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from priceguessr.models import Users

#აუტენფიკაციის და პაროლის ჰაშის კოდი

password_hasher = PasswordHasher() # არგონ2-ის  ჰაშერის ობიექტი
#სხვათაშორის ეს ჰაშერი და კოდები youtube-ში ვნახე :)

class AuthManager:
    def __init__(self, database):
        self.database = database
    def signup(self, username, password): #sign up
        password_hash = password_hasher.hash(password) #ვჰაშავთ პაროლს
        conn = self.database.connect()


        try:
            cursor = conn.cursor()

            prompt = """INSERT INTO users (username, password) VALUES (?, ?)"""
            cursor.execute(prompt, (username, password_hash)) # ვავსებთ მომხმარებლის მონაცემებს
            conn.commit()

            return Users(cursor.lastrowid, username) #მოგვაქვს user ობიექტი აიდით და სახელით
        finally:
            conn.close() # ვხურავთ კავშირს

    def login(self, username, password):


        conn = self.database.connect()
        try:
            cursor = conn.cursor()
            prompt = """SELECT * FROM users WHERE username = ?"""
            cursor.execute(prompt, (username,))
            row = cursor.fetchone() # მოგვაქვს მომხამრებელი
        finally:
            conn.close()
        if row is None:
            return None
        try:
        

            password_hasher.verify(row["password"], password) # ვამოწმებთ ერთია თუ არა
        
        except (VerifyMismatchError, InvalidHashError): # თუ არა მაშინ აბრუნებს ერორს
            return None

        return Users(row["id"], row["username"]) #გვიბრუნებს მომხმარებლის აიდის და სახელს
