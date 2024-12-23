import filemanager
import os
import datetime
from datetime import date
from datetime import datetime
import keyboard




parancsok = {
    "help":"megjeleníti ezt a felületet.",
    "delete":"töröl egy fájlt név szerint. használat: delete [bejegyzéscím]",
    "edit":"szerkeszt név szerint egy üzenetet. használat: edit [bejegyzéscím], ezután adja az új címet és a bejegyzés új tartalmát: [bejegyzéscím]; [bejegyzéstartalom]",
    "create":"létrehoz egy új bejegyzést. használat: create [bejegyzéscím]; [bejegyzéstartalom]",
    "list":"listázza az összes bejegyzést használata: list [szűrés] szűrési lehetőségek: kész(a készen lévő bejegyzések) folyamatban(a folyamatban lévő bejegyzések) heti(a héten esedékes/határidős bejegyzések) a szűrési érték list után írásával csak a szűrésnek megfelelő bejegyzések jelennek majd meg",
    "open":"megnyit egy bejegyzést cím alapján használata: open [bejegyzéscím]",
    "done":"készre állítja egy bejegyzés állapotát használat: done [bejegyzéscím]",
    "Egyéb megjegyzések":"Kérjük a dátumokat ÉÉÉÉ.HH.NN formátumban adja meg. példa: 2025.01.01",
}

def GetUnameGetHash(u_name= "alap_user", hash= "alap_hash"):
    global username
    username = u_name

    global passwordHash
    passwordHash = hash


def ListElvalasztoGeneralas():
    # bejegyzes_cimek = filemanager.UserStored(username: str)
    bejegyzes_cim_datum_allapot = [["bejegyzes1", "2024.10.12", "kész"], ["bejegyzes2", "2024.10.13", "kész"], ["bejegyzes3", "2024.11.15", "folyamatban"], ["bejegyzes4", "2024.12.10", "folyamatban"], ["bejegyzes5", "2024.12.20", "folyamatban"], ["bejegyzes6", "2024.12.22", "folyamatban"]]
    bejegyzes_cimek = []

    for csomag in bejegyzes_cim_datum_allapot:
        bejegyzes_cimek.append(csomag[0])

    elvalaszto = ""

    for _ in max(bejegyzes_cimek, key=len):
        elvalaszto += "─"

    return elvalaszto

def AdatElvalasztoGeneralas(string):
    adatelvalaszto = "─"

    for _ in string:
        adatelvalaszto += "─"

    return adatelvalaszto

def Help(parancs_parameterk):
    os.system('cls')

    for parancs, magyarazat in parancsok.items():
        print(f"{parancs} - {magyarazat}\n")

def Delete(parancs_parameterek): # Meghívja a fájlkezelés | törlési funkcióját |
    os.system('cls')
    # Itt is bekérjük a címeket 
    # bejegyzes_cim_datum_allapot = filemanager.UserStored(mefelelő paraméterek)
    bejegyzes_cim_datum_allapot = [["bejegyzes1", "2024.10.12", "kész"], ["bejegyzes2", "2024.10.13", "kész"], ["bejegyzes3", "2024.11.15", "folyamatban"], ["bejegyzes4", "2024.12.10", "folyamatban"], ["bejegyzes5", "2024.12.20", "folyamatban"], ["bejegyzes6", "2024.12.22", "folyamatban"]]
    cimek = []

    for csomag in bejegyzes_cim_datum_allapot:
        cimek.append(csomag[0])

    torolendo = parancs_parameterek[1]

    if torolendo in cimek:
        print("Töröltük a bejegyzést")
        filemanager.Delete(username, passwordHash, torolendo)
    elif torolendo not in cimek:
        print("Nem található ilyen bejegyzés!")

def Edit(parancs_parameterek): # Meghívja a fájlkezelés | szerkesztési funkcióját |
    os.system('cls')

    szerkesztendo = parancs_parameterek[1]

    # Itt is bekérjük a címeket filemanager.UserStored(mefelelő paraméterek)
    bejegyzes_cim_datum_allapot = [["bejegyzes1", "2024.10.12", "kész"], ["bejegyzes2", "2024.10.13", "kész"], ["bejegyzes3", "2024.11.15", "folyamatban"], ["bejegyzes4", "2024.12.10", "folyamatban"], ["bejegyzes5", "2024.12.20", "folyamatban"], ["bejegyzes6", "2024.12.22", "folyamatban"]]
    cimek = []

    for csomag in bejegyzes_cim_datum_allapot:
        cimek.append(csomag[0])

    # adatok = filemanager.Read(username, passwordHash, szerkesztendo) a megfelelő paraméterekkel
    adatok = ["cim", "2024.01.01", "bejegyzestartalom", "folyamatban"] 

    if szerkesztendo in cimek:

        allapot = adatok.pop()

        adatsor = ""

        for adat in adatok:
            adatsor += adat
            if adatok.index(adat) != 2:
                adatsor += "; "

        print(f"\nEredeti Bejegyzés és adatai:                 {adatsor}\n")

        parancs_parameterek = input("Kérem adja meg az új bejegyzési adatokat --> ")

        try:
            bejegyzesadatok = parancs_parameterek.split("; ")
            cim = bejegyzesadatok.pop(0).replace(" ", "")
            datum = bejegyzesadatok.pop(0).replace(" ", "")
            bejegyzestartalom = " ".join(bejegyzesadatok)

            print(cim, datum)
            print(bejegyzestartalom)

            datum_felbontva = datum.split(".")

            if len(datum_felbontva) == 3 and len(datum_felbontva[1]) == 2 and 0 < int(datum_felbontva[1]) <= 31 and 0 < int(datum_felbontva[2]) < 31 and len(datum_felbontva[2]) == 2:
                print("\nA bejegyzését rögzítettük.")

                # Ezután továbbítjuk a címet dátumot és a tartalmat rögzítésre
                filemanager.Edit(username, passwordHash, cim, datum, bejegyzestartalom, allapot)
            else:
                print("\nHelytelenül adta meg a dátumot vagy helytelenül választotta el a bejegyzés elemeit! Nem mentettük a változásokat")

        except IndexError:
            print("\nHelytelen volt a bejegyzés elemeinek elválasztása. Nem mentettük a változásokat")

        except ValueError:
            print("Helytelenül volt megadva a parancs. Nem mentettük a változásokat")
    
    elif adatok[0] not in cimek:
        print("Nem létezik ilyen bejegyzés")

def Create(parancs_parameterek): # Megívja a fájlkezelés | létrehozás funkcióját |
    # Itt is bekérjük a címeket filemanager.UserStored(mefelelő paraméterek)

    os.system('cls')

    bejegyzes_cim_datum_allapot = [["bejegyzes1", "2024.10.12", "kész"], ["bejegyzes2", "2024.10.13", "kész"], ["bejegyzes3", "2024.11.15", "folyamatban"], ["bejegyzes4", "2024.12.10", "folyamatban"], ["bejegyzes5", "2024.12.20", "folyamatban"], ["bejegyzes6", "2024.12.22", "folyamatban"]]
    cimek = []

    for csomag in bejegyzes_cim_datum_allapot:
        cimek.append(csomag[0])

    try:
        parancs_parameterek[0] = ""

        bejegyzesadatok = " ".join(parancs_parameterek).split("; ")

        cim = bejegyzesadatok.pop(0).replace(" ", "")
        datum = bejegyzesadatok.pop(0).replace(" ", "")

        if cim not in cimek:

            bejegyzestartalom = " ".join(bejegyzesadatok)

            datum_felbontva = datum.split(".")

            if len(datum_felbontva) == 3 and len(datum_felbontva[1]) == 2 and 0 < int(datum_felbontva[1]) <= 31 and 0 < int(datum_felbontva[2]) < 31 and len(datum_felbontva[2]) == 2:
                print("\nA bejegyzését rögzítettük.")

                # Ezután továbbítjuk a címet dátumot és a tartalmat rögzítésre
                #filemanager.Store(username, passwordHash, cim, datum, bejegyzestartalom)
            else:
                print("\nHelytelenül adta meg a dátumot vagy helytelenül választotta el a bejegyzés elemeit!. Nem mentettük a változásokat")

        elif cim in cimek:
            print("Már létezik ilyen nevű bejegyzés. Nem mentettük a változásokat")

    except IndexError:
        print("\nHelytelen volt a bejegyzés elemeinek elválasztása. Nem mentettük a változásokat")
    
    except ValueError:
        print("Helytelenül volt megadva a parancs. Nem mentettük a változásokat")

def SzuresFolyamatban(bejegyzes_cim_datum_allapot):
    print(f"Folyamatban lévő bejegyzések\n")
    print(f"{ListElvalasztoGeneralas()}")
    for csomag in bejegyzes_cim_datum_allapot:
        if csomag[2] == "folyamatban":
            print(f"{csomag[0]} határidő: {csomag[1]} [{csomag[2]}]")
            print(f"{ListElvalasztoGeneralas()}")

def SzuresKesz(bejegyzes_cim_datum_allapot):
    print(f"Kész bejegyzések\n")
    print(f"{ListElvalasztoGeneralas()}")

    for csomag in bejegyzes_cim_datum_allapot:
        if csomag[2] == "kész":
            print(f"{csomag[0]} határidő: {csomag[1]} [{csomag[2]}]")
            print(f"{ListElvalasztoGeneralas()}")

def SzuresHeti(bejegyzes_cim_datum_allapot):
    print(f"A Héten határidős bejegyzések\n")
    print(f"{ListElvalasztoGeneralas()}")

    mai_datum = date.today()
    aktualis_het = mai_datum.isocalendar()[1]

    for csomag in bejegyzes_cim_datum_allapot:
        csomag_het = datetime.strptime(csomag[1], "%Y.%m.%d").date().isocalendar()[1]

        if aktualis_het == csomag_het:
            print(f"{csomag[0]} határidő: {csomag[1]} [{csomag[2]}]")
            print(f"{ListElvalasztoGeneralas()}")

def Done(parancs_parameterek):
    # Itt is bekérjük a címeket filemanager.UserStored(mefelelő paraméterek)

    cim = parancs_parameterek[1]

    bejegyzes_cim_datum_allapot = [["bejegyzes1", "2024.10.12", "kész"], ["bejegyzes2", "2024.10.13", "kész"], ["bejegyzes3", "2024.11.15", "folyamatban"], ["bejegyzes4", "2024.12.10", "folyamatban"], ["bejegyzes5", "2024.12.20", "folyamatban"], ["bejegyzes6", "2024.12.22", "folyamatban"]]
    cimek = []

    for csomag in bejegyzes_cim_datum_allapot:
        cimek.append(csomag[0])

    #adatok = filemanager.Read(username, passwordHash, cim)

    os.system('cls')

    if cim in cimek:
        #filemanager.Edit(username, passwordHash, adatok[2], "kész")
        print(f"\nKészre állítottuk a következő bejegyzést: {cim}")

    elif cim not in cimek:
        print("Nem létezik ilyen bejegyzés")


def List(parancs_parameterek): # Bejegyzés | címek listázása |
    # bejegyzes_cimek = filemanager.UserStored(username: str)

    bejegyzes_cim_datum_allapot = [["bejegyzes1", "2024.10.12", "kész"], ["bejegyzes2", "2024.10.13", "kész"], ["bejegyzes3", "2024.11.15", "folyamatban"], ["bejegyzes4", "2024.12.10", "folyamatban"], ["bejegyzes5", "2024.12.20", "folyamatban"], ["bejegyzes6", "2024.12.22", "folyamatban"]]

    os.system('cls')


    if len(parancs_parameterek) == 2:
        print("Bejegyzések\n")
        print(f"{ListElvalasztoGeneralas()}")

        for csomag in bejegyzes_cim_datum_allapot:
            print(f"{csomag[0]} határidő: {csomag[1]} [{csomag[2]}]")
            print(f"{ListElvalasztoGeneralas()}")
    elif 4 > len(parancs_parameterek) > 2:
        szures_tipus = parancs_parameterek[1].capitalize()

        eval("Szures"+szures_tipus.replace("é", "e")+f"({bejegyzes_cim_datum_allapot})")


def Open(parancs_parameterek): # Kért | bejegyzés megnyitása |
    bejegyzes_cim_datum_allapot = [["bejegyzes1", "2024.10.12", "kész"], ["bejegyzes2", "2024.10.13", "kész"], ["bejegyzes3", "2024.11.15", "folyamatban"], ["bejegyzes4", "2024.12.10", "folyamatban"], ["bejegyzes5", "2024.12.20", "folyamatban"], ["bejegyzes6", "2024.12.22", "folyamatban"]]
    bejegyzes_cimek = []

    for csomag in bejegyzes_cim_datum_allapot:
        bejegyzes_cimek.append(csomag[0])

    megnyitando_bejegyzes = parancs_parameterek[1]
    os.system('cls')
    
    bejegyzes_tartalom = "Általános bejegyzéstartalom Általános bejegyzéstartalom" # Ennek a helyére ez jön majd: filemanager.Read(username: str, passwordHash: b, title: str, text: str) a megfelelő paraméterekkel
    

    if megnyitando_bejegyzes != "" and megnyitando_bejegyzes in bejegyzes_cimek:
        print(f"| {megnyitando_bejegyzes} | Határidő: {bejegyzes_cim_datum_allapot[bejegyzes_cimek.index(megnyitando_bejegyzes)][1]} [{bejegyzes_cim_datum_allapot[bejegyzes_cimek.index(megnyitando_bejegyzes)][2]}]")
        print(f"  {ListElvalasztoGeneralas()}")
        print(f"\n{bejegyzes_tartalom}")

GetUnameGetHash()

while True: # Fő Loop
    user_input = input(f"\n{username} --> ")
    user_input = user_input.split(" ")
    user_input[0] = user_input[0].capitalize()
    user_input.append("")

    try:
        eval(user_input[0] + f"({user_input})")

    except NameError:
        print("Helytelen volt az input")

    except TypeError:
        print("Hiányzik egy parancsrész")
