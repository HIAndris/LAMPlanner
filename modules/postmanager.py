import filemanager
import os
import datetime
from datetime import date
from datetime import datetime
from unittest.mock import patch

parancsok = {
    "help":"megjeleníti ezt a felületet.",
    "delete":"töröl egy fájlt név szerint. használat: delete [bejegyzéscím]",
    "edit":"szerkeszt név szerint egy üzenetet. használat: edit [bejegyzéscím], ezután adja az új címet és a bejegyzés új tartalmát: [bejegyzéscím]; [bejegyzéstartalom]",
    "create":"létrehoz egy új bejegyzést. használat: create [bejegyzéscím]; [bejegyzéstartalom]",
    "list":"listázza az összes bejegyzést használata: list [szűrés] szűrési lehetőségek: kész(a készen lévő bejegyzések) folyamatban(a folyamatban lévő bejegyzések) heti(a héten esedékes/határidős bejegyzések) a szűrési érték list után írásával csak a szűrésnek megfelelő bejegyzések jelennek majd meg",
    "open":"megnyit egy bejegyzést cím alapján használata: open [bejegyzéscím]",
    "done":"készre állítja egy bejegyzés állapotát használat: done [bejegyzéscím]"
}

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
    pass

def Edit(parancs_parameterek): # Meghívja a fájlkezelés | szerkesztési funkcióját |
    pass

def Create(parancs_parameterek): # Megívja a fájlkezelés | létrehozás funkcióját |
    pass

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

def KesszeAlakitas():
    pass


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

while True:
    user_input = input("\nfelhasználónév --> ")
    user_input = user_input.split(" ")
    user_input[0] = user_input[0].capitalize()
    user_input.append("")

    try:
        eval(user_input[0] + f"({user_input})")

    except NameError:
        print("Helytelen volt az input")

    except TypeError:
        print("Hiányzik egy parancsrész")
