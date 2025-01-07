from modules import filemanager
import os

os.system('cls')

parancsok = {
    "help":"megjeleníti ezt a felületet.",
    "delete":"töröl egy fájlt név szerint. használat: delete [bejegyzéscím]",
    "edit":"szerkeszt cím szerint egy bejegyzést. használat: edit [bejegyzéscím], ezután adja az új címet és a bejegyzés új határidejét: [bejegyzéscím]; [határidő] ezután a szerkesztőfelületen adja meg a bejegyzés új taralmát",
    "create":"létrehoz egy új bejegyzést. használat: create [bejegyzéscím]; [határidő] ezután a szerkesztőfelületen rögzítheti a bejegyzés tartalmát",
    "list":"listázza az összes bejegyzést használata: list [szűrés] szűrési lehetőségek: kész(a készen lévő bejegyzések) folyamatban(a folyamatban lévő bejegyzések) heti(a héten esedékes/határidős bejegyzések) a szűrési érték list után írásával csak a szűrésnek megfelelő bejegyzések jelennek majd meg",
    "open":"megnyit egy bejegyzést cím alapján használata: open [bejegyzéscím]",
    "done":"készre állítja egy bejegyzés állapotát használat: done [bejegyzéscím]",
    "undone":"folyamatban lévőre állítja egy bejegyzés állapotát használat: undone [bejegyzéscím]",
    "Egyéb megjegyzések":"Kérjük a dátumokat ÉÉÉÉ.HH.NN formátumban adja meg. példa: 2025.01.01",
    "logout":"Kijelentkezés"
}

def GetUnameGetHash(u_name, u_password):
    global username
    username = u_name

    global userid
    userid = filemanager.GetUserSerial(username)

    global decryption_key
    decryption_key = filemanager.CreateEncryptionKey(u_name, u_password)


def ListElvalasztoGeneralas():
    elvalaszto = ""

    for _ in range(os.get_terminal_size().columns):
        elvalaszto += "-"

    return elvalaszto

def Help(parancs_parameterk):
    os.system('cls')

    for parancs, magyarazat in parancsok.items():
        print(f"{parancs}:")
        print(f"{magyarazat}")
        print(ListElvalasztoGeneralas(), end="")
        
def Delete(parancs_parameterek): # Meghívja a fájlkezelés | törlési funkcióját |
    os.system('cls')
    cimek = filemanager.GetUserStored(userid, decryption_key)

    torolendo = parancs_parameterek[1]

    if torolendo in cimek:
        if input(f"\nBiztosan törölni akaja a(z) {torolendo} nevű bejegyzést? (igen/nem) --> ") == "igen":
            print("Töröltük a bejegyzést.")
            filemanager.Delete(userid, decryption_key, torolendo)
        else:
            print("Nem töröltük a bejegyzést.")
    elif torolendo not in cimek:
        print("Nem található ilyen bejegyzés.")

def SzerkesztFelulet(cim, datum, bejegyzestartalom=""):
    bejegyzestartalom = ""
    sor = " "

    os.system('cls')

    print("Szerkesztőfelület \n-----------------\n\nKérem adja meg a bejegyzés tartalmát, a következő sorba lépéshez nyomjon entert és a befejezéshez üssön 2 entert (hagyja az utolsó sort üresen)\n")

    while sor != "":
        sor = input()
        bejegyzestartalom += f"{sor}\n"

    os.system('cls')

    return cim, datum, bejegyzestartalom



def Edit(parancs_parameterek): # Meghívja a fájlkezelés | szerkesztési funkcióját |
    os.system('cls')

    szerkesztendo = parancs_parameterek[1]

    bejegyzes_cim_datum_allapot = filemanager.GetUserStored(userid, decryption_key, "p")
    cimek = []

    for csomag in bejegyzes_cim_datum_allapot:
        cimek.append(csomag[0])

    adatok = filemanager.Read(userid, decryption_key, szerkesztendo)

    if szerkesztendo in cimek:
        cimek.remove(szerkesztendo)
        
        adatsor = (f"Cím: {adatok['title']}; Határidő: {adatok['date']} \n\n{adatok['text']}")

        print(f"Szerkesztőfelület \n-----------------\n\nEredeti Bejegyzés és adatai: \n\n{adatsor}\n")
        parancs_parameterek = input("Kérem adja meg az új bejegyzési címet és határidőt --> ")

        try:
            bejegyzesadatok = parancs_parameterek.split("; ")

            datum = bejegyzesadatok.pop().replace(" ", "")
            cim = "; ".join(bejegyzesadatok) 
            datum_felbontva = datum.split(".")

            if len(datum_felbontva) == 3 and len(datum_felbontva[1]) == 2 and 0 < int(datum_felbontva[1]) <= 12 and 0 < int(datum_felbontva[2]) <= 31 and len(datum_felbontva[2]) == 2 and int(datum_felbontva[0]) > 0:
                if cim not in cimek:
                    cim, datum, bejegyzestartalom = SzerkesztFelulet(cim, datum, adatok["status"])

                    print(f"Új Cím: {cim}, Új Dátum: {datum}\n")
                    print(bejegyzestartalom)

                    # Ezután továbbítjuk a címet dátumot és a tartalmat rögzítésre

                    filemanager.EditProperties(userid, decryption_key, adatok['title'], cim, datum)
                    filemanager.EditText(userid, decryption_key, cim, bejegyzestartalom)

                    print("------------------------\nBejegyzését rögzítettük.")
                else:
                    print("Már létezik ilyen nevű bejegyzés")


            else:
                print("\nHelytelenül adta meg a dátumot vagy helytelenül választotta el a bejegyzés elemeit! Nem mentettük a változásokat.")


        except ValueError:
            print("Helytelenül volt megadva a parancs. Nem mentettük a változásokat.")

        except IndexError:
            print("\nHelytelen volt a bejegyzés elemeinek elválasztása. Nem mentettük a változásokat")
    
    else:
        print("Nem létezik ilyen bejegyzés.")

def Create(parancs_parameterek): # Megívja a fájlkezelés | létrehozás funkcióját |
    # Itt is bekérjük a címeket 
    cimek = filemanager.GetUserStored(userid, decryption_key)

    os.system('cls')

    try:
        parancs_parameterek.pop(0)

        bejegyzesadatok = " ".join(parancs_parameterek).split("; ")

        datum = bejegyzesadatok.pop().replace(" ", "")
        cim = "; ".join(bejegyzesadatok) 
        datum_felbontva = datum.split(".")

        print(f"Bejegyzés címe: {cim}, Határidő: {datum}")

        if cim not in cimek:
            if len(datum_felbontva) == 3 and len(datum_felbontva[1]) == 2 and 0 < int(datum_felbontva[1]) <= 12 and 0 < int(datum_felbontva[2]) <= 31 and len(datum_felbontva[2]) == 2 and int(datum_felbontva[0]) > 0:
                cim, datum, bejegyzestartalom = SzerkesztFelulet(cim, datum)

                print(f"Cím: {cim}, Határidő: {datum}\n")
                print(bejegyzestartalom)

                # Ezután továbbítjuk a címet dátumot és a tartalmat rögzítésre
                filemanager.Store(userid, decryption_key, cim, bejegyzestartalom, datum)

                print("------------------------\nBejegyzését rögzítettük.")
                

            else:
                print("\nHelytelenül adta meg a dátumot vagy helytelenül választotta el a bejegyzés elemeit!. Nem mentettük a változásokat")

        elif cim in cimek:
            print("Már létezik ilyen nevű bejegyzés. Nem mentettük a változásokat")
    
    except ValueError:
            print("\nHelytelen volt a bejegyzés elemeinek elválasztása, vagy a dátum megadása. Nem mentettük a változásokat")

    except IndexError:
        print("\nHelytelen volt a bejegyzés elemeinek elválasztása. Nem mentettük a változásokat")
    
    
def BiztonsagosPrint(csomag):
    szelesseg = os.get_terminal_size().columns
    if csomag[2] == True:
        csomag[2] = "Kész"
    else:
        csomag[2] = "Folyamatban"

    adatok = f"{csomag[0]} | határidő: {csomag[1]} | [{csomag[2]}]"
    if len(adatok) > szelesseg:
        karakter_helyek = len(adatok) - (len(adatok) - szelesseg) - 3
        for karakter in range(karakter_helyek):
            print(adatok[karakter], end="")
        print("...")
        print(f"\n{ListElvalasztoGeneralas()}")
    else:
        print(adatok)
        print(f"{ListElvalasztoGeneralas()}")

def SzuresSzamlalo(megjelenitesi_szamlalo):
    if megjelenitesi_szamlalo > 0:
        print(f"\n{megjelenitesi_szamlalo}db szűrésnek megfelelő elem van")
    else:
        print("\nNincs a szűrésnek megfelelő elem")

def SzuresFolyamatban(bejegyzes_cim_datum_allapot):
    megjelenitesi_szamlalo = 0
    print(f"Folyamatban lévő bejegyzések\n")
    print(f"{ListElvalasztoGeneralas()}")

    for csomag in bejegyzes_cim_datum_allapot:
        if csomag[2] == False:
            BiztonsagosPrint(csomag)
            megjelenitesi_szamlalo += 1

    return megjelenitesi_szamlalo


def SzuresKesz(bejegyzes_cim_datum_allapot):
    megjelenitesi_szamlalo = 0
    print(f"Kész bejegyzések\n")
    print(f"{ListElvalasztoGeneralas()}")

    for csomag in bejegyzes_cim_datum_allapot:
        if csomag[2] == True:
            BiztonsagosPrint(csomag)
            megjelenitesi_szamlalo += 1

    return megjelenitesi_szamlalo


def SzuresHeti(bejegyzes_cim_datum_allapot):
    from datetime import datetime

    megjelenitesi_szamlalo = 0
    print(f"A Héten határidős bejegyzések\n")
    print(f"{ListElvalasztoGeneralas()}")

    mai_datum = datetime.today()
    aktualis_ev = datetime.today().year
    aktualis_het = mai_datum.isocalendar()[1]

    for csomag in bejegyzes_cim_datum_allapot:
        csomag_het = datetime.strptime(csomag[1], "%Y.%m.%d").date().isocalendar()[1]
        csomag_ev = datetime.strptime(csomag[1], "%Y.%m.%d").date().year

        if aktualis_het == csomag_het and csomag_ev == aktualis_ev:
            BiztonsagosPrint(csomag)
            megjelenitesi_szamlalo += 1

    return megjelenitesi_szamlalo

    

def Done(parancs_parameterek):
    cim = parancs_parameterek[1]

    os.system('cls')

    edit = filemanager.EditProperties(userid, decryption_key, parancs_parameterek[1], newStatus = True)
    
    if edit:
        print(f"\nKészre állítottuk a következő bejegyzést: {cim}")
    else:
        print(f"Nincs ilyen bejegyzés! ({cim})")

def Undone(parancs_parameterek):
    cim = parancs_parameterek[1]

    os.system('cls')

    edit = filemanager.EditProperties(userid, decryption_key, parancs_parameterek[1], newStatus = False)
    
    if edit:
        print(f"\nFolyamatban lévőre állítottuk a következő bejegyzést: {cim}")
    else:
        print(f"Nincs ilyen bejegyzés! ({cim})")
    
    
def List(parancs_parameterek): # Bejegyzés | címek listázása |
    megjelenitesi_szamlalo = 0
    bejegyzes_cim_datum_allapot = filemanager.GetUserStored(userid, decryption_key, "pl")
    
    os.system('cls')

    if len(parancs_parameterek) == 2:
        print("Bejegyzések\n")
        print(f"{ListElvalasztoGeneralas()}")

        for csomag in bejegyzes_cim_datum_allapot:
            BiztonsagosPrint(csomag)
            megjelenitesi_szamlalo += 1

        
    elif 4 > len(parancs_parameterek) > 2:
        szures_tipus = parancs_parameterek[1].capitalize()

        megjelenitesi_szamlalo = eval("Szures"+szures_tipus.replace("é", "e")+f"({bejegyzes_cim_datum_allapot})")
    
    SzuresSzamlalo(megjelenitesi_szamlalo)


def Open(parancs_parameterek): # Kért | bejegyzés megnyitása |
    bejegyzes_cimek = filemanager.GetUserStored(userid, decryption_key)    

    megnyitando_bejegyzes = parancs_parameterek[1]
    os.system('cls')
    
    bejegyzes_adatok = filemanager.Read(userid, decryption_key, megnyitando_bejegyzes)
    bejegyzes_cim = bejegyzes_adatok["title"]
    bejegyzes_tartalom = bejegyzes_adatok["text"]
    bejegyzes_datum = bejegyzes_adatok["date"]
    bejegyzes_status = bejegyzes_adatok["status"]

    if bejegyzes_status == True:
        bejegyzes_status = "Kész"
    else:
        bejegyzes_status = "Folyamatban"

    if megnyitando_bejegyzes in bejegyzes_cimek:
        print(f"| {bejegyzes_cim} | Határidő: {bejegyzes_datum} [{bejegyzes_status}]")
        print(f"{ListElvalasztoGeneralas()}")
        print(f"\n{bejegyzes_tartalom}")

def MainLoop(user_input):
        # Fő Loop
        
        try:
            eval(user_input[0] + f"({user_input})")

        except NameError as e:
            os.system("cls")
            print(f"Helytelen volt az input. ({e})")

        except ValueError as e:
            os.system("cls")
            print(f"Helytelen volt az input. ({e})")
