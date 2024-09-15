from tkinter import *
from tkinter import messagebox as ms
from base_window import BaseWindow
import random
import time
# from user import UserScreen
from ship_placer import ShipPlacer


class BattleshipGame(BaseWindow):
    def __init__(self, master, user_data):
        super().__init__(master)

        self.user_data = user_data
        self.setup_window = None
        self.username = user_data[1]
        self.db.increment_games_played(self.user_data[1])
        self.ship_placer = ShipPlacer()
        self.setup_screen()
        self.update_time_id = None

    def setup_screen(self):
        self.setup_window = Toplevel(self.master)
        self.setup_window.title("Ustawienie Statków")
        self.setup_window.geometry("500x650")

        self.player_grid = [[0] * 10 for _ in range(10)]
        self.ships = [(5, "Carrier"), (4, "Battleship"), (3, "Cruiser"), (3, "Submarine"), (2, "Destroyer")]

        Label(self.setup_window, text="Ustaw swoje statki", font=("Calibri", 14)).pack()
        Label(self.setup_window, text="Przykład poprawnego formatu współrzędnych:", font=("Calibri", 11)).pack()
        Label(self.setup_window, text="'A3H' albo 'B4V', gdzie H to poziomo a V to pionowo",
              font=("Calibri", 11)).pack()

        self.entries = []
        for i, (size, name) in enumerate(self.ships):
            frame = Frame(self.setup_window)
            frame.pack(pady=5)
            Label(frame, text=f"{name} ({size} cells): ").pack(side=LEFT)
            entry = Entry(frame)
            entry.pack(side=LEFT)
            self.entries.append(entry)

        self.status_label = Label(self.setup_window, text="", fg="red")
        self.status_label.pack()

        Button(self.setup_window, text="Ustaw statki", command=self.place_ships).pack(pady=20)
        Button(self.setup_window, text="PLAY", command=self.start_game).pack()

        self.canvas = Canvas(self.setup_window, width=350, height=350)
        self.canvas.pack(pady=20)
        self.draw_grid(self.canvas, self.player_grid, 30)

    def draw_grid(self, canvas, grid, cell_size):
        canvas.delete("all")

        for i in range(10):
            canvas.create_text(15, i * cell_size + 30, text=str(i + 1), anchor="center")
            canvas.create_text(i * cell_size + 45, 15, text=chr(ord('A') + i), anchor="center")

        for i in range(10):
            for j in range(10):
                x0, y0 = j * cell_size + 30, i * cell_size + 30
                x1, y1 = x0 + cell_size, y0 + cell_size
                color = "blue"
                if grid[i][j] == 1:
                    color = "gray"
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def place_ships(self):
        self.player_grid = [[0] * 10 for _ in range(10)]
        for entry, (size, name) in zip(self.entries, self.ships):
            data = entry.get().strip().upper()
            if not data or len(data) < 3:
                self.status_label.config(text=f"Niepoprawne dane dla {name}")
                return

            col, row, orientation = data[0], data[1:-1], data[-1]
            if not col.isalpha() or not row.isdigit() or orientation not in "HV":
                self.status_label.config(text=f"Niepoprawne dane dla {name}")
                return

            col = ord(col) - ord('A')
            row = int(row) - 1
            if not (0 <= col < 10 and 0 <= row < 10):
                self.status_label.config(text=f"Niepoprawne dane dla {name}")
                return

            if not self.ship_placer.can_place_ship(self.player_grid, row, col, size, orientation):
                self.status_label.config(text=f"Nie można umieścić {name} w tej pozycji")
                return

            self.ship_placer.add_ship_to_grid(self.player_grid, row, col, size, orientation)

        self.status_label.config(text="Statki zostały ustawione poprawnie", fg="green")
        self.draw_grid(self.canvas, self.player_grid, 30)

    def start_game(self):
        self.setup_window.destroy()
        self.game_screen()
        self.start_time = time.time()  # Rozpoczęcie odliczania czasu
        self.update_time()  # Rozpoczęcie aktualizacji czasu

    def game_screen(self):
        self.game_window = Toplevel(self.master)
        self.game_window.title("Battleship")

        self.player_grid_canvas = Canvas(self.game_window, width=350, height=350)
        self.player_grid_canvas.pack(side=LEFT, padx=20, pady=20)
        self.draw_grid(self.player_grid_canvas, self.player_grid, 30)

        self.opponent_grid = [[0] * 10 for _ in range(10)]
        self.opponent_grid_canvas = Canvas(self.game_window, width=350, height=350)
        self.opponent_grid_canvas.pack(side=RIGHT, padx=20, pady=20)
        self.draw_grid(self.opponent_grid_canvas, self.opponent_grid, 30)

        self.opponent_grid_canvas.bind("<Button-1>", self.player_shoot)
        self.place_computer_ships()

        self.time_label = Label(self.game_window, text="Time: 00:00", font=("Calibri", 12))
        self.time_label.pack()

    def place_computer_ships(self):
        self.computer_ships = []
        for size, name in self.ships:
            placed = False
            while not placed:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice("HV")
                if self.ship_placer.can_place_ship(self.opponent_grid, row, col, size, orientation):
                    self.ship_placer.add_ship_to_grid(self.opponent_grid, row, col, size, orientation)
                    self.computer_ships.append((row, col, size, orientation))
                    placed = True

    def player_shoot(self, event):
        cell_size = 30
        col = (event.x - 30) // cell_size
        row = (event.y - 30) // cell_size
        if 0 <= row < 10 and 0 <= col < 10:
            if self.opponent_grid[row][col] == 1:
                self.opponent_grid[row][col] = 2
                self.opponent_grid_canvas.create_rectangle(col * cell_size + 30, row * cell_size + 30,
                                                           (col + 1) * cell_size + 30, (row + 1) * cell_size + 30,
                                                           fill="red")
                self.check_win()
            elif self.opponent_grid[row][col] == 0:
                self.opponent_grid[row][col] = -1
                self.opponent_grid_canvas.create_rectangle(col * cell_size + 30, row * cell_size + 30,
                                                           (col + 1) * cell_size + 30, (row + 1) * cell_size + 30,
                                                           fill="yellow")
                self.computer_turn()

    def computer_turn(self):
        row, col = -1, -1
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if self.player_grid[row][col] in {0, 1}:
                break

        if self.player_grid[row][col] == 1:
            self.player_grid[row][col] = 2
            self.player_grid_canvas.create_rectangle(col * 30 + 30, row * 30 + 30, (col + 1) * 30 + 30,
                                                     (row + 1) * 30 + 30, fill="red")
        else:
            self.player_grid[row][col] = -1
            self.player_grid_canvas.create_rectangle(col * 30 + 30, row * 30 + 30, (col + 1) * 30 + 30,
                                                     (row + 1) * 30 + 30, fill="yellow")

        self.check_win()

    def check_win(self):
        if all(cell != 1 for row in self.player_grid for cell in row):
            ms.showinfo("Koniec gry", "Komputer wygrał!")
            self.game_window.destroy()
            self.stop_time()
            self.go_to_user_screen(self.user_data)
        elif all(cell != 1 for row in self.opponent_grid for cell in row):
            print(self.user_data[5])
            self.db.increment_games_won(self.user_data)
            print(self.user_data[5])

            ms.showinfo("Koniec gry", "Wygrałeś!")
            self.game_window.destroy()
            self.stop_time()
            self.go_to_user_screen(self.user_data)

    def set_user_screen(self, user_screen):
        self.user_screen = user_screen

    def go_to_user_screen(self, user_data):
        if self.setup_window and self.setup_window.winfo_exists():
            self.setup_window.destroy()
        if self.game_window and self.game_window.winfo_exists():
            self.game_window.destroy()

        # Przywrócenie okna użytkownika
        if self.user_screen:
            self.user_screen.show_user_screen()

        from user import UserScreen
        UserScreen(self.master, self.user_data)

    def update_time(self):
        current_time = time.time() - self.start_time
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        time_str = f"Time: {minutes:02}:{seconds:02}"
        self.time_label.config(text=time_str)
        self.update_time_id = self.game_window.after(1000, self.update_time)

    def stop_time(self):
        if self.update_time_id is not None:
            self.game_window.after_cancel(self.update_time_id)