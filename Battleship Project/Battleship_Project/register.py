from tkinter import *
from tkinter import messagebox as ms
import re
from base_window import BaseWindow

class RegisterScreen(BaseWindow):
    def __init__(self, master):
        super().__init__(master)

        self.register_screen = Toplevel(master)
        self.register_screen.title("Rejestracja")
        self.register_screen.geometry("400x300")
        Label(self.register_screen, text="Podaj swoje dane rejestracji", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()

        self.username = StringVar()
        self.password1 = StringVar()
        self.password2 = StringVar()
        self.email = StringVar()

        Label(self.register_screen, text="Wprowadz nazwe uzytkownika i haslo, a nastepnie powtorz haslo").pack()
        Label(self.register_screen, text="").pack()

        username_label = Label(self.register_screen, text="Nazwa uzytkownika*")
        username_label.pack()

        self.username_entry = Entry(self.register_screen, textvariable=self.username)
        self.username_entry.pack()

        email_label = Label(self.register_screen, text="Email*")
        email_label.pack()

        self.email_entry = Entry(self.register_screen, textvariable=self.email)
        self.email_entry.pack()

        password_label = Label(self.register_screen, text="Haslo*")
        password_label.pack()

        self.password1_entry = Entry(self.register_screen, textvariable=self.password1, show='*')
        self.password1_entry.pack()

        password2_label = Label(self.register_screen, text="Powtorz haslo*")
        password2_label.pack()

        self.password2_entry = Entry(self.register_screen, textvariable=self.password2, show='*')
        self.password2_entry.pack()

        Button(self.register_screen, text="Zarejestruj", width=10, height=1, bg="blue", command=self.register_user).pack()

    def validate_password(self):
        password = self.password1.get()
        password_repeat = self.password2.get()

        pattern = r'^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.{8,})'
        if not re.match(pattern, password):
            ms.showerror("Error", "Password must contain at least one uppercase letter, one special character, and be at least 8 characters long.")
            return False

        if password != password_repeat:
            ms.showerror("Blad", "Podane hasla nie sa identyczne.")
            return False

        return True


    def register_user(self):
        if self.validate_password():
            username = self.username.get()
            password = self.password1.get()
            email = self.email.get()
            self.db.insert_user(username, password, email)
            ms.showinfo("Sukces", "Rejestracja udana!")