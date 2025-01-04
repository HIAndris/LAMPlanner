from modules import postmanager
from modules import usermanager
from modules import filemanager
import os

running = True
loggedIn = False
username = ""
password = ""

os.system("cls")
print("Üdvözöljük! Válasszon az opciók közül!")
while running:
    if not loggedIn:
        print(usermanager.ElvalasztoGeneralas() + "\nlogin: bejelentkezés\nsignup: regisztráció\ndelete: felhasználó törlése\nexit: kilépés a programból\n" + usermanager.ElvalasztoGeneralas())
        choice = input("Nincs bejelentkezve --> ")

        if choice == "login":
            os.system("cls")
            username, password, loggedIn = usermanager.LogIn()

            if loggedIn:
                postmanager.GetUnameGetHash(username, password)
                password = ""
            else:
                print("Válasszon az opciók közül!")
        
        elif choice == "delete":
            os.system("cls")
            usermanager.Delete()
            
        elif choice == "signup":
            username, password, loggedIn = usermanager.SignUp()

            if loggedIn:
                postmanager.GetUnameGetHash(username, password)
                password = ""
            else:
                print("Válasszon az opciók közül!")

        elif choice == "exit":
            running = False
            
        else:
            os.system("cls")
            print("Válasszon az opciók közül!")
            
    if loggedIn:
        user_input = input(f"\n{username} --> ")

        if user_input != "logout":
            user_input = user_input.split(" ", 1)
            user_input[0] = user_input[0].capitalize()
            user_input.append("")

            postmanager.MainLoop(user_input)
        else:
            loggedIn = False
