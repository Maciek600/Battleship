from tkinter import *
from login import LoginScreen
from register import RegisterScreen
from tkinter import messagebox as ms

#Konta (nazwa, hasło):
#Admin: Admin, Adminek123
#Tester: Tester, T3$T3r2005
class MainScreen:
    def __init__(self):
        self.logo_image = None
        self.main_screen = Tk()
        self.main_screen.geometry("500x400")
        self.main_screen.title("Logowanie")


        self.load_logo()

        Button(text="Login", height="2", width="30", bg="blue", command=self.login).pack()
        Label(text="").pack()

        Button(text="Register", height="2", width="30", bg="red", command=self.register).pack()

        self.main_screen.mainloop()

    def load_logo(self):
        try:
            self.logo_image = PhotoImage(file="logo.png")
            logo_label = Label(self.main_screen, image=self.logo_image)
            logo_label.pack(pady=10)  # Add padding for spacing
        except Exception as e:
            ms.showerror("Błąd", f"Nie udało się załadować obrazka: {e}")
            
    def login(self):

        LoginScreen(self.main_screen)

    def register(self):
        RegisterScreen(self.main_screen)
    


if __name__ == "__main__":
    MainScreen()
