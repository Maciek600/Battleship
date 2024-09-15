import sqlite3
from tkinter import messagebox as ms
import threading


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('usersDB.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS "users" (
            "user_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "username" TEXT NOT NULL UNIQUE,
            "password" TEXT NOT NULL,
            "email" TEXT NOT NULL UNIQUE,
            "games_played" INTEGER DEFAULT 0,
            "games_won" INTEGER DEFAULT 0
        )''')
        self.conn.commit()

    def insert_user(self, username, password, email):
        def task():
            try:
                self.cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                                 (username, password, email))
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                ms.showerror("Error", f"Użytkownik o tej nazwie lub email już istnieje: {e}")
            except Exception as e:
                ms.showerror("Database Error", f"An error occurred: {e}")

        thread = threading.Thread(target=task)
        thread.start()

    def fetch_user(self, username):
        self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cur.fetchone()

    def fetch_all_users(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def fetch_user_by_email(self, email):
        self.cur.execute("SELECT * FROM users WHERE email=?", (email,))
        return self.cur.fetchone()

    def update_password(self, username, new_password):
        def task():
            self.cur.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
            self.conn.commit()

        thread = threading.Thread(target=task)
        thread.start()

    def increment_games_played(self, username):
        def task():
            self.cur.execute("SELECT games_played FROM users WHERE username=?", (username,))
            result = self.cur.fetchone()
            if result:
                games_played = result[0] + 1
                self.cur.execute("UPDATE users SET games_played=? WHERE username=?", (games_played, username))
                self.conn.commit()

        thread = threading.Thread(target=task)
        thread.start()

    def increment_games_won(self, user_data):

                print(user_data[5])
                games_won = user_data[5] + 1
                print(games_won)
                self.cur.execute("UPDATE users SET games_won=? WHERE username=?", (games_won, user_data[1]))
                self.conn.commit()



    def delete_user(self, user_id):
        def task():
            self.cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
            self.conn.commit()

        thread = threading.Thread(target=task)
        thread.start()

    def user_exists(self, user_id):
        self.cur.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
        return self.cur.fetchone() is not None