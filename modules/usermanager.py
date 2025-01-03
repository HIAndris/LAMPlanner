import os
import filemanager

USER_DATA_FILE = "users.txt"

def Load_Users(): #felhasználói adatok betöltése
    users = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    username, password, other_data = line.split("|")
                    users[username] = {"password": password, "other_data": other_data}
    return users

def Delete_Users(): #felhasználói adatok törlése
    print("Felhasználó törlési felület")
    username = input("Adja meg a törlendő felhasználó nevét: ")

    users = Load_Users()

    #ellenőrizzük, hogy létezik-e a felhasználó
    if username not in users:
        print("Felhasználónév nem található!")
        return False

    #törlés
    success = filemanager.DeleteUser(username, users[username]["password"])  #meghívjuk a DeleteUser alprogramot
    if success:
        print(f"A(z) {username} felhasználó sikeresen törlésre került!")
    else:
        print("A felhasználó törlése nem sikerült.")
    
    return success

def Register(): #regisztrációs felület és folyamat létrehozása
    print("Regisztrációs felület")
    username = input("Adja meg a felhasználónevét: ")
    password = input("Adja meg a jelszavát: ")
    other_data = input("Adjon meg egyéb adatokat (pl. email, telefonszám): ")

    users = Load_Users()

    #ellenőrizzük, hogy már létezik-e ilyen felhasználónév
    if username in users:
        print("Ez a felhasználónév már foglalt.")
        return False

    #felhasználó adatainak mentése
    success = filemanager.SignUp(username, password)  #meghívjuk a SignUp alprogramot
    if success:
        print("Sikeres regisztráció!")
    else:
        print("A regisztráció nem sikerült.")
    
    return success

def Login(): #bejelentkezési felület és folyamat létrehozása
    print("Bejelentkezési felület")
    username = input("Adja meg a felhasználónevét: ")
    password = input("Adja meg a jelszavát: ")

    success = filemanager.LogIn(username, password)  #meghívjuk a LogIn alprogramot
    if success:
        print("Sikeres bejelentkezés!")
    else:
        print("Hibás felhasználónév vagy jelszó!")
    
    return success

def Main(): #regisztrációs, bejelentkezési és törlési felület kiválasztása, main programegység
    while True:
        print("\nVálasszon egy lehetőséget:")
        print("1. Regisztráció")
        print("2. Bejelentkezés")
        print("3. Felhasználó törlése")
        print("4. Kilépés")
        
        choice = input("Választás (1/2/3/4): ")
        
        if choice == "1":
            success = Register()
            if not success:
                print("A regisztráció nem sikerült. Próbálja újra.")
        elif choice == "2":
            success = Login()
            if not success:
                print("A bejelentkezés nem sikerült. Próbálja újra.")
        elif choice == "3":
            success = Delete_Users()
            if not success:
                print("A felhasználó törlése nem sikerült. Próbálja újra.")
        elif choice == "4":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás, próbálja újra.")

if __name__ == "__main__":
    Main()
