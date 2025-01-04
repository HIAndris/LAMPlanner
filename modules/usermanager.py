from modules import filemanager
import os

def PasswordCreation() -> str:
    import os
    import sys

    def ClearLineBack(n: int = 1):
        for _ in range(n):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[2K")
        sys.stdout.flush()

    spec = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    print("Válasszon jelszót!")

    correct = False
    while not correct:
        password = input("-" * os.get_terminal_size().columns + "\nJelszó --> ")
        print("\033[F", "Jelszó --> ", "*" * (len(password)), sep = "")
        passwordLen = len(password)

        if passwordLen <= 5:
            ClearLineBack(3)
            print(f"Túl rövid! (5-től 30 karakterig terjedhet, {passwordLen} karakter megadva)")

        elif 30 <= passwordLen:
            ClearLineBack(3)
            print(f"Túl hosszú! (5-től 30 karakterig terjedhet, {passwordLen} karakter megadva)")

        elif not any(char.isupper() for char in password):
            ClearLineBack(3)
            print("Nem tartalmaz nagybetűt!")

        elif not any(char.islower() for char in password):
            ClearLineBack(3)
            print("Nem tartalmaz kisbetűt!")

        elif not any(char in spec for char in password):
            ClearLineBack(3)
            print("Nem tartalmaz speciális karaktert!")

        elif not any(char.isdigit() for char in password):
            ClearLineBack(3)
            print("Nem tartalmaz számot!")

        else:
            repeatPassword = input("-" * os.get_terminal_size().columns + "\nJelszó ismét --> ")
            print("\033[F", "Jelszó ismét --> ", "*" * (len(repeatPassword)), sep = "")

            if repeatPassword != password:
                ClearLineBack(5)
                print("A két jelszó nem egyezik!")

            else:
                correct = True

    return password


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

            else:
                os.system("cls")
                print(f"Helytelen Jelszó, próbálja újra\n{ElvalasztoGeneralas()}")

        elif username not in users and username != "":
            os.system("cls")
            print(f"Nem létezik {username} felhasználó!\n{ElvalasztoGeneralas()}")

    return "", "", False


def SignUp():
    import os

    users = filemanager.Users()

    correct = False
    os.system("cls")
    while not correct:
        name = input("Felhasználónév (hagyja üresen a visszalépéshez) --> ")
        nameLen = len(name)

        if name == "":
            return "", "", False

        elif name in users:
            os.system("cls")
            print("Már létező felhasználó!\n" + "-" * os.get_terminal_size().columns)

        elif 20 < nameLen:
            os.system("cls")
            print(f"Túl hosszú! (maximum 20 karakter, {nameLen} karakter megadva)" + "\n" + "-" * os.get_terminal_size().columns)

        else:
            correct = True

    print("-" * os.get_terminal_size().columns)
    password = PasswordCreation()

    signup = filemanager.SignUp(name, password)

    if signup:
        login = filemanager.LogIn(name, password)

        if login:
            os.system("cls")
            print("Sikeres regisztráció! Üdvözöljük! Használja a help parancsot a parancssegédlet megjelenítéséhez!\n")

            return name, password, True

        else:
            RuntimeError("Logging in was not successful! :/ (this should not happen)")
    else:
        RuntimeError("Signing up was not successful! :/ (this should not happen)")


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
