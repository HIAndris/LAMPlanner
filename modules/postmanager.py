import filemanager
import os
from unittest.mock import patch

parancsok = {
    "help":"megjeleníti ezt a felületet.",
    "delete":"töröl egy fájlt név szerint. használat: delete [bejegyzéscím]",
    "edit":"szerkeszt név szerint egy üzenetet. használat: edit [bejegyzéscím], ezután adja az új címet és a bejegyzés új tartalmát: [bejegyzéscím]; [bejegyzéstartalom]",
    "create":"létrehoz egy új bejegyzést. használat: create [bejegyzéscím]; [bejegyzéstartalom]"
}

def Help(parancs_parameterk):
    for parancs, magyarazat in parancsok.items():
        print(f"{parancs} - {magyarazat}")

def Delete(parancs_parameterek): # Meghívja a fájlkezelés | törlési funkcióját |
    pass

def Edit(parancs_parameterek): # Meghívja a fájlkezelés | szerkesztési funkcióját |
    pass

def Create(parancs_parameterek): # Megívja a fájlkezelés | létrehozás funkcióját |
    pass

def List(parancs_parameterek): # Bejegyzés | címek listázása |
    # bejegyzes_cimek = filemanager.UserStored(username: str)
    bejegyzes_cimek = ["bejegyzes1", "bejegyzes2", "bejegyzes3", "bejegyzes4", "bejegyzes5"]
    os.system('cls')

    elvalaszto = "──"

    for _ in max(bejegyzes_cimek, key=len):
        elvalaszto += "─"

    print("Bejegyzések\n")
    print(elvalaszto)

    for cim in bejegyzes_cimek:
        print(f" {cim}")
        print(f"{elvalaszto}")


def Open(parancs_parameterek): # Kért | bejegyzés megnyitása |
    pass

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