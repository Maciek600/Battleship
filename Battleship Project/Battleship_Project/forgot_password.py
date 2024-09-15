from tkinter import *
from tkinter import messagebox as ms
import re
from base_window import BaseWindow

class ForgotPasswordScreen(BaseWindow):
    def __init__(self, master):
        super().__init__(master)

        self.forgot_password_screen = Toplevel(master)
        self.forgot_password_screen.title("Odzyskiwanie hasła")
        self.forgot_password_screen.geometry("400x300")
        Label(self.forgot_password_screen, text="Odzyskiwanie hasła", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()

        self.username = StringVar()
        self.email = StringVar()
        self.new_password1 = StringVar()
        self.new_password2 = StringVar()
        self.auth_code = StringVar()

        Label(self.forgot_password_screen, text="Nazwa uzytkownika*").pack()
        self.username_entry = Entry(self.forgot_password_screen, textvariable=self.username)
        self.username_entry.pack()

        Label(self.forgot_password_screen, text="Email*").pack()
        self.email_entry = Entry(self.forgot_password_screen, textvariable=self.email)
        self.email_entry.pack()

        Label(self.forgot_password_screen, text="Nowe hasło*").pack()
        self.new_password1_entry = Entry(self.forgot_password_screen, textvariable=self.new_password1, show='*')
        self.new_password1_entry.pack()

        Label(self.forgot_password_screen, text="Powtórz nowe hasło*").pack()
        self.new_password2_entry = Entry(self.forgot_password_screen, textvariable=self.new_password2, show='*')
        self.new_password2_entry.pack()

        Label(self.forgot_password_screen, text="Kod autoryzacyjny*").pack()
        self.auth_code_entry = Entry(self.forgot_password_screen, textvariable=self.auth_code)
        self.auth_code_entry.pack()

        Button(self.forgot_password_screen, text="Resetuj hasło", width=15, height=1, bg="blue", command=self.reset_password).pack()

    def validate_password(self):
        password = self.new_password1.get()
        password_repeat = self.new_password2.get()

        pattern = r'^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.{8,})'
        if not re.match(pattern, password):
            ms.showerror("Error", "Password must contain at least one uppercase letter, one special character, and be at least 8 characters long.")
            return False

        if password != password_repeat:
            ms.showerror("Blad", "Podane hasla nie sa identyczne.")
            return False

        return True

    def reset_password(self):
        if not self.validate_password():
            return

        username = self.username.get()
        email = self.email.get()
        new_password = self.new_password1.get()
        auth_code = self.auth_code.get()

        user_data = self.db.fetch_user(username)

        if not user_data or user_data[3] != email:
            ms.showerror("Error", "Nazwa użytkownika lub email są niepoprawne.")
            return

        if auth_code != "123456":
            ms.showerror("Error", "Kod autoryzacyjny jest niepoprawny.")
            return

        self.db.update_password(username, new_password)
        ms.showinfo("Sukces", "Hasło zostało zresetowane.")