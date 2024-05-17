from datetime import datetime, date, timedelta
from abc import ABC, abstractmethod
import random
import time
import os
import re

class Szoba(ABC):
    ar = 0
    szobaszam = 0

    def __init__(self, szobaszam):
        self.szobaszam = szobaszam
class EgyagyasSzoba(Szoba):
    ar = 2000
    agyakSz = 1

class KetagyasSzoba(Szoba):
    ar = 3500
    agyakSz = 2

class Szalloda:
    nev = ""
    szobak = []

    def __init__ (self, nev):
        szobak = []
        for i in range(0, random.randint(3,10)):
            egyagyas = random.randint(0,1) == 1

            szoba = False
            if egyagyas:
                szoba = EgyagyasSzoba(i)
            else:
                szoba = KetagyasSzoba(i)

            szobak.append(szoba)

        self.nev = nev
        self.szobak = szobak


class Foglalas:
    nev = ""
    szobaszam = 0
    bejelentkezes = ""
    kijelentkezes = ""

    def __init__(self, nev, szobaszam, bejelent, kijelent):
        if not Szalloda.szobak[szobaszam]:
            return False

        self.nev = nev
        self.szobaszam = szobaszam
        self.bejelentkezes = bejelent
        self.kijelentkezes = kijelent

        return Szalloda.szobak[szobaszam].ar




szalloda = Szalloda("Project Szálloda")



foglalasok = []
def foglalaslemondas(foglalasID):
    if not foglalasID:
        return False

    foglalasok.pop(int(foglalasID))
    return True

def foglalashozzaadasa(nev,szobaszam,datum):
    if not nev or not szobaszam or not datum:
        return False

    adat = {
        'nev' : nev,
        'szobaszam' : szobaszam,
        'datum' : datum,
        'ar' : szalloda.szobak[szobaszam].ar,
        'agyakSz' : szalloda.szobak[szobaszam].agyakSz,
    }
    foglalasok.append(adat)

    return szalloda.szobak[szobaszam].ar

def foglalasoklistazasa(showID):
    if len(foglalasok) == 0:
        print("Jelenleg nincs egy foglalás sem!")
        return

    foglalasID = 1
    for foglalas in foglalasok:
        if showID:
            print(f'foglalásID: {foglalasID}, szobaszám: {foglalas['szobaszam']}, foglalva: {foglalas['datum']}, név: {foglalas['nev']}, ágyak száma: {foglalas['agyakSz']}, ár: {foglalas['ar']}Ft')
        else:
            print(f'szobaszám: {foglalas['szobaszam']}, foglalva: {foglalas['datum']}, név: {foglalas['nev']}, ágyak száma: {foglalas['agyakSz']}, ár: {foglalas['ar']}Ft')

        foglalasID += 1

foglalashozzaadasa('Rugós Beke', 1, '2025-10-10')
foglalashozzaadasa('Kis Miklós', 1, '2025-10-15')
foglalashozzaadasa('Lakatos Brendon', 2, '2025-10-10')





feluletek = ['|Foglalás', ' |Lemondás', ' |Listázás',' |Kilépés']
def cleanFelulet():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def getInput(szoveg, szam):
    ertek = ""
    while ertek == "" or (szam and not re.match(r"^[0-9]+$", ertek)):
        ertek = input(szoveg)

    return ertek

def feluletresze(felulet):
    cleanFelulet()

    if felulet == 0:
        print(f' |Üdvözöllek a {szalloda.nev} recepciós menüjében.|')

        szoveg = ""
        for i in range(0, len(feluletek)):
            name = feluletek[i]
            if not name:
                continue

            szoveg += f'{name}: {i+1}'
        print(szoveg)

        feluletID = int(getInput('Válassza ki a kívánt opciót: ', True))
        while feluletID < 1 or feluletID > len(feluletek):
            feluletID = int(getInput("Válassza ki a kívánt opciót: ", True))

        feluletresze(feluletID)
    elif felulet == 1:
        print("Szobák: ")
        for szoba in szalloda.szobak:
            print(f'  |szobaszám: {szoba.szobaszam}, ár: {szoba.ar}Ft, Ágyak száma: {szoba.agyakSz}|')

        nev = getInput('Adja meg a nevét ékezetek nélkül: ', False)
        while not re.match(r'[A-Za-z]+ [A-Za-z]+', nev):
            nev = getInput('Adja meg a nevét ékezetek nélkül: ', False)

        szabadszoba = False
        while not szabadszoba:
            szobaszam = int(getInput('Válassz szobaszámot: ', True))
            while szobaszam < 0 or szobaszam > len(szalloda.szobak) - 1:
                szobaszam = int(getInput('Válassz szobaszámot: ', True))

            datum = getInput('Válassz dátumot: ', False)
            while not re.match(r"\b(19\d\d|20\d\d)[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b",datum) or datetime.strptime(datum, '%Y-%m-%d').date() < date.today():
                datum = getInput('Válassz dátumot: ', False)

            talalat = False
            for foglalas in foglalasok:
                if foglalas['szobaszam'] == szobaszam:
                    foglaltDatum = datetime.strptime(foglalas['datum'], '%Y-%m-%d').date()
                    bekertDatum = datetime.strptime(datum, '%Y-%m-%d').date()

                    if foglaltDatum == bekertDatum or foglaltDatum + timedelta(days=1) == bekertDatum or bekertDatum - timedelta(days=-1) == foglaltDatum:
                        talalat = True
                        break

            szabadszoba = not talalat

            if not szabadszoba:
                print('Ez a szoba már levan foglalva az adott időpontra!')
                time.sleep(1)

        result = foglalashozzaadasa(nev, szobaszam, datum)
        if result:
            print('Foglalás sikeres!')
            print(f'Szoba ára: {result}Ft')

        time.sleep(2)
        feluletresze(0)
    elif felulet == 2:
        foglalasoklistazasa(True)
        print('Visszalépéshez irja be a 0-át.')

        foglalasID = int(getInput('Válassz foglalást!: ', True))
        while foglalasID < 0 or foglalasID > len(foglalasok):
            foglalasID = int(getInput('Válassz foglalást!: ', True))

        if foglalasID == 0:
            feluletresze(0)

        foglalasID -= 1
        foglalas = foglalasok[foglalasID]
        print(f'szobaszám: {foglalas['szobaszam']}, foglalva: {foglalas['datum']}, ágyak száma: {foglalas['agyakSz']}, ár: {foglalas['ar']}Ft')

        ertek = getInput('Biztosan szeretné törölni a foglalást? Kérem |igen| vagy |nem| opció közü válasszon!: ', False)
        while ertek != 'igen' and ertek != 'nem':
            ertek = getInput('Biztosan szeretné törölni a foglalást? Kérem |igen| vagy |nem| opció közü válasszon!: ', False)

        if ertek == 'igen':
            foglalaslemondas(foglalasID)
            feluletresze(0)
            print("A foglalás törlése sikeresen végrehajtódott")
        else:
            feluletresze(2)
    elif felulet == 3:
        foglalasoklistazasa(False)
        print('Visszalépés: 0')

        ertek = int(getInput('Válassz az opciók közül: ', True))
        while ertek != 0:
            ertek = int(getInput('Válassz az opciók közül: ', True))

        felulet = ertek
        feluletresze(felulet)
    elif felulet == 4:
        print('Viszont látásra! Vissza várjuk.')
        time.sleep(2)
        cleanFelulet()
        exit()

def Main():
    feluletresze(0)

Main()