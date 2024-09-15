from tkinter import Toplevel, Label, Button, Frame
from base_window import BaseWindow
import time
from battleship import BattleshipGame

class UserScreen(BaseWindow):
    def __init__(self, master, user_data):
        super().__init__(master)

        self.user_data = user_data
        self.username = user_data[1]
        self.games_played = user_data[4]
        self.games_won = user_data[5]

        self.user_screen = Toplevel(master)
        self.user_screen.title("Panel użytkownika")
        self.user_screen.geometry("500x400")

        Label(self.user_screen, text=f"Witaj, {self.username}", font=("Calibri", 14)).pack()

        self.time_label = Label(self.user_screen, font=("Calibri", 12))
        self.time_label.pack()

        Button(self.user_screen, text="Start Game", width=10, height=1, bg="blue", command=self.start_game).pack()
        Label(self.user_screen, text="").pack()

        Button(self.user_screen, text="Exit", width=10, height=1, bg="red", command=self.user_screen.destroy).pack()

        self.update_time()
        self.create_stats_table()

    def update_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.config(text=current_time)
        self.user_screen.after(1000, self.update_time)

    def create_stats_table(self):
        stats_frame = Frame(self.user_screen)
        stats_frame.pack(pady=10)

        headers = ["Statystyka", "Wartość"]
        data = [
            ["Liczba rozegranych gier", self.games_played],
            ["Liczba wygranych gier", self.games_won]
        ]

        for i, header in enumerate(headers):
            label = Label(stats_frame, text=header, font=("Calibri", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        for i, row in enumerate(data, start=1):
            for j, value in enumerate(row):
                label = Label(stats_frame, text=value, font=("Calibri", 12))
                label.grid(row=i, column=j, padx=5, pady=5)

    def start_game(self):
        self.user_screen.withdraw()
        game = BattleshipGame(self.master, self.user_data)
        game.set_user_screen(self)

    def show_user_screen(self):
        self.user_screen.deiconify()