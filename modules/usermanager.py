from modules import filemanager
import os

def ElvalasztoGeneralas():
    szelesseg = os.get_terminal_size().columns
    elvalaszto = ""

    for _ in range(szelesseg):
        elvalaszto += "-"

    return elvalaszto

def LogIn():
    users = filemanager.Users("u")

    username = " "
    login = False

    while not login and username != "":
        password = ""
        

        username = input("Felhasználónév (hagyja üresen a visszalépéshez) --> ")

        if username in users:
            password = input(f"{ElvalasztoGeneralas()}\nJelszó --> ")

            login = filemanager.LogIn(username, password)

            if login:
                os.system("cls")
                print("Sikeres bejelentkezés! Üdvözöljük! Használja a help parancsot a parancssegédlet megjelenítéséhez!\n") 

                return username, password, True
                # Mehet a postmanager
            else:
                os.system("cls")
                print(f"Helytelen Jelszó, próbálja újra\n{ElvalasztoGeneralas()}")

        elif username not in users and username != "":
            os.system("cls")
            print(f"Nem létezik {username} felhasználó!\n{ElvalasztoGeneralas()}")

    return "", "", False
    

def Delete():
    users = filemanager.Users("u")

    username = input("Törölni kívánt fiók felhasználóneve (hagyja üresen a visszalépéshez) --> ")

    if username in users:
        password = input(f"{ElvalasztoGeneralas()}\nTörölni kívánt fiók jelszava --> ")

        os.system("cls")

        if input(f"\nBiztosan törölni akaja a {username} nevű fiókot? (igen/nem) --> ") == "igen":
            deleted = filemanager.DeleteUser(username, password)

            if deleted:
                os.system("cls")
                print("Felhasználó sikeresen törölve")
            else:
                os.system("cls")
                print(f"Helytelen Jelszó, próbálja újra\n{ElvalasztoGeneralas()}")
                Delete()
        else:
            os.system("cls")
            print("Nem töröltünk fiókot.")

    elif username == "":
        os.system("cls")
        print("Nem töröltünk felhasználót")

    else:
        os.system("cls")
        print(f"Nem létezik {username} felhasználó!\n{ElvalasztoGeneralas()}")
        Delete()
