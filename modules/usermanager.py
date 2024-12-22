import json
import os

def Load_Users(): #felhasználói adatok betöltése
  pass

def Delete_Users(): #felhasználói adatok törlése
  pass

def Register(): #regisztrációs felület és folyamat létrehozása
  print("Regisztrációs felület")
    username = input("Adja meg a felhasználónevét: ")
    password = input("Adja meg a jelszavát: ")
    other_data = input("Adjon meg egyéb adatokat (pl. email, telefonszám): ")

    users = Load_users()

def Login(): #bejelentkezési felület és folyamat létrehozása
   print("Bejelentkezési felület")
    username = input("Adja meg a felhasználónevét: ")
    password = input("Adja meg a jelszavát: ")

    users = load_users()

def Main(): #regisztrációs és bejelentkezési felület kiválasztása, main programegység
  while True:
    print("\nVálasszon egy lehetőséget:")
        print("1. Regisztráció")
        print("2. Bejelentkezés")
        print("3. Kilépés")
        
        choice = input("Választás (1/2/3): ")
        
        if choice == "1":
            success = Register()
            if not success:
                print("A regisztráció nem sikerült. Próbálja újra.")
        elif choice == "2":
            success = Login()
            if not success:
                print("A bejelentkezés nem sikerült. Próbálja újra.")
        elif choice == "3":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás, próbálja újra.")
