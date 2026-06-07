from priceguessr.models import Users

class AuthManager:
    def __init__(self,database):
        self.database = database

    def signup(self,username,password):
        conn = self.database.connect()
        cursor = conn.cursor()
        prompt = """
        INSERT INTO users (username,password) VALUES (?,?)
        """
        cursor.execute(prompt,(username,password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return Users(user_id,username)
    def login(self,username,password):
        conn = self.database.connect()
        cursor = conn.cursor()
        prompt = """
        Select * from users where users.username = ? AND users.password = ?
        """
        cursor.execute(prompt,(username,password))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return Users(row['id'],row['username'])

        