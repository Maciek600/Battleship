from tkinter import *
from tkinter import messagebox as ms
from base_window import BaseWindow

class AdminScreen(BaseWindow):
    def __init__(self, master):
        super().__init__(master)
        self.show_screen()

    def show_screen(self):
        self.admin_screen = Toplevel(self.master)
        self.admin_screen.title("Admin Panel")
        self.admin_screen.geometry("600x400")
        Label(self.admin_screen, text="Admin Panel", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()

        # Frame to hold listbox and delete user input
        frame = Frame(self.admin_screen)
        frame.pack(pady=20)

        # Listbox to display users
        self.users_list = Listbox(frame, width=90)
        self.users_list.pack(side=LEFT, fill=Y)

        # Scrollbar for listbox
        scrollbar = Scrollbar(frame, orient=VERTICAL)
        scrollbar.config(command=self.users_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.users_list.config(yscrollcommand=scrollbar.set)

        self.delete_entry = Entry(self.admin_screen, width=30)
        self.delete_entry.pack()

        self.load_users()

        Button(self.admin_screen, text="Usuń wybranego użytkownika", command=self.delete_user).pack()
        Label(text="").pack()

        Button(self.admin_screen, text="Exit", width=10, height=1, bg="red", command=self.admin_screen.destroy).pack()

    def load_users(self):
        self.users_list.delete(0, END)
        users = self.db.fetch_all_users()
        for user in users:
            self.users_list.insert(END, f"ID: {user[0]}, Username: {user[1]}, Email: {user[3]}, Games Played: {user[4]}, Games Won: {user[5]}")

    def delete_user(self):
        user_id = self.delete_entry.get()
        if user_id.strip().isdigit():
            user_id = int(user_id.strip())
            if self.db.user_exists(user_id):
                self.db.delete_user(user_id)
                ms.showinfo("Sukces", f"Użytkownik o ID {user_id} został usunięty.")
                self.load_users()
                self.delete_entry.delete(0, END)
            else:
                ms.showerror("Błąd", f"Użytkownik o ID {user_id} nie istnieje.")
        else:
            ms.showerror("Błąd", "Wpisz poprawne ID użytkownika.")
