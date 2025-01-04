from modules import postmanager
from modules import usermanager
from modules import filemanager
import os

running = True
loggedIn = False
username = ""

while running:
    if not loggedIn:
        os.system("cls")
        choice = input("Nincs bejelentkezve --> ")

        if choice == "login":
            os.system("cls")
            username, password, loggedIn = usermanager.LogIn()
        elif choice == "delete":
            os.system("cls")
            usermanager.Delete()
        elif choice == "signup":
            username, password, loggedIn = usermanager.SignUp()
        elif choice == "exit":
            break
    
    if loggedIn:
        postmanager.GetUnameGetHash(username, password)

        user_input = input(f"\n{username} --> ")

        if user_input != "logout":
            user_input = user_input.split(" ", 1)
            user_input[0] = user_input[0].capitalize()
            user_input.append("")

            postmanager.MainLoop(user_input)
        else:
            loggedIn = False
