from database import Database


class BaseWindow:
    def __init__(self, master):
        self.master = master
        self.db = Database()

    def start_game(self):
        pass

    def show_screen(self):
        pass
