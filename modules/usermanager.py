from modules import filemanager
import os

def ValidatePassword():
    pass

def LogIn():
    login = False

    users = filemanager.Users("u")

    username = " "

    while not login and username != "":
        username = input("Felhasználónév (hagyja üresen a visszalépéshez) --> ")

        if username in users:
            password = input("----------------------------------------------\nJelszó --> ")

            login = filemanager.LogIn(username, password)

            if login:
                os.system("cls")
                print("Sikeres bejelentkezés, Üdvözöljük! Használja a help parancsot a parancssegédlet megjelenítéséhez\n") 

                return username, password, True
                # Mehet a postmanager
            else:
                os.system("cls")
                print("Helytelen Jelszó, próbálja újra\n-------------------------------\n")

        elif username not in users and username != "":
            os.system("cls")
            print("Nem létezik ilyen felhasználó!\n------------------------------\n")

    return "", "", False


def SignUp():
    pass

def Delete():
    users = filemanager.Users("u")

    username = input("Törölni kívánt fiók felhasználóneve (hagyja üresen a visszalépéshez) --> ")

    if username in users:
        password = input("--------------------------------------------------------------------\nTörölni kívánt fiók jelszava --> ")

        os.system("cls")

        if input(f"\nBiztosan törölni akaja a {username} nevű fiókot? (igen/nem) --> ") == "igen":
            deleted = filemanager.DeleteUser(username, password)

            if deleted:
                os.system("cls")
                print("Felhasználó sikeresen törölve")
            else:
                os.system("cls")
                print("Helytelen Jelszó, próbálja újra\n-------------------------------\n")
                Delete()
        else:
            os.system("cls")
            print("Nem töröltünk fiókot.")

    elif username == "":
        os.system("cls")
        print("Nem töröltünk felhasználót")

    else:
        os.system("cls")
        print("Nem létezik ilyen felhasználó!\n------------------------------\n")
        Delete()


filemanager.SignUp("Jóska", "Jelszó")
