from tkinter import *
from tkinter import messagebox as ms
from base_window import BaseWindow
from admin import AdminScreen
from user import UserScreen
from forgot_password import ForgotPasswordScreen

class LoginScreen(BaseWindow):
    def __init__(self, master):
        super().__init__(master)

        self.login_screen = Toplevel(master)
        self.login_screen.title("Logowanie")
        self.login_screen.geometry("400x300")
        Label(self.login_screen, text="Podaj swoje dane logowania", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        
        self.username = StringVar()
        self.password = StringVar()

        Label(self.login_screen, text="Enter username and password").pack()
        Label(self.login_screen, text="").pack()

        username_label = Label(self.login_screen, text="Username*")
        username_label.pack()

        self.username_entry = Entry(self.login_screen, textvariable=self.username)
        self.username_entry.pack()

        password_label = Label(self.login_screen, text="Password*")
        password_label.pack()

        self.password_entry = Entry(self.login_screen, textvariable=self.password, show='*')
        self.password_entry.pack()

        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Login", width=10, height=1, bg="blue", command=self.login).pack()
        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Forgot Password?", width=15, height=1, bg="blue", command=self.forgot_password).pack()

    def login(self):
        username = self.username.get()
        password = self.password.get()

        if username == "Admin" and password == "Adminek123":
            ms.showinfo("Success", "Login successful!")
            self.login_screen.destroy()
            AdminScreen(self.master)
        else:
            user_data = self.db.fetch_user(username)
            if user_data:
                if user_data[2] == password:
                    ms.showinfo("Success", "Login successful!")
                    self.login_screen.destroy()
                    UserScreen(self.master, user_data)
                else:
                    ms.showerror("Error", "Incorrect password.")
            else:
                ms.showerror("Error", "User not found.")

    def forgot_password(self):
        ms.showinfo("Kod weryfikacyjny", "Twój kod weryfikacyjny to: 123456")
        ForgotPasswordScreen(self.master)
