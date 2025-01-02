import os

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

    users = load_users()

    #ellenőrizzük, hogy létezik-e a felhasználó
    if username not in users:
        print("Felhasználónév nem található!")
        return False

    #törlés
    del users[username]
    save_users(users)
    
    print(f"A(z) {username} felhasználó sikeresen törlésre került!")
    return True

def Register(): #regisztrációs felület és folyamat létrehozása
  print("Regisztrációs felület")
    username = input("Adja meg a felhasználónevét: ")
    password = input("Adja meg a jelszavát: ")
    other_data = input("Adjon meg egyéb adatokat (pl. email, telefonszám): ")

    users = Load_users()

#ellenőrizzük, hogy már létezik-e ilyen felhasználónév
    if username in users:
        print("Ez a felhasználónév már foglalt.")
        return False

    #felhasználó adatainak mentése
    users[username] = {"password": password, "other_data": other_data}
    save_users(users)
    
    print("Sikeres regisztráció!")
    return True

def Login(): #bejelentkezési felület és folyamat létrehozása
   print("Bejelentkezési felület")
    username = input("Adja meg a felhasználónevét: ")
    password = input("Adja meg a jelszavát: ")

    users = load_users()

    #ellenőrizzük a felhasználói adatokat
    if username not in users:
        print("Felhasználónév nem található!")
        return False

    #ellenőrizzük a jelszót
    if users[username]["password"] != password:
        print("Hibás jelszó!")
        return False
      
def Main(): #regisztrációs, bejelentkezési és törlési felület kiválasztása, main programegység
  while True:
        print("\nVálasszon egy lehetőséget:")
        print("1. Regisztráció")
        print("2. Bejelentkezés")
        print("3. Felhasználó törlése")
        print("4. Kilépés")
        
        choice = input("Választás (1/2/3/4): ")
        
        if choice == "1":
            success = register()
            if not success:
                print("A regisztráció nem sikerült. Próbálja újra.")
        elif choice == "2":
            success = login()
            if not success:
                print("A bejelentkezés nem sikerült. Próbálja újra.")
        elif choice == "3":
            success = delete_user()
            if not success:
                print("A felhasználó törlése nem sikerült. Próbálja újra.")
        elif choice == "4":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás, próbálja újra.")

if __name__ == "__main__":
    main()
