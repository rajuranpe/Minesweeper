#-*- coding: utf-8 -*-    
#Tämä tiedosto on pelimoduuli, pelataksesi suorita valikko.py
 
import random
import time
import datetime
 
def kysy_kentan_muoto():
    """Tarkistetaan kentän koko- ja miinamäärä-syötteiden oikeellisuus, melko monihaarainen jotta jokaiseen virheeseen saadaan oikeanlainen ohje. Maksimikoko kentälle on 20 koska tämän jälkeen alkaa mennä aika hasardin näköiseksi konsolissa."""
    global leveys, korkeus
    while True:
        try:
            leveys, korkeus, miinamaara = raw_input("Syötä kentän leveys, korkeus ja miinamäärä muodossa \"leveys,korkeus,miinamäärä\", leveys ja korkeus samat ja välillä 3 ja 20 ja miinoja niin että ne miinat mahtuvat kentälle: ").split(",")    
        except ValueError:
            print "Koitapas uusiksi, muodossa \"LEVEYS,KORKEUS,MIINAMÄÄRÄ\"."
            continue
        else:
            try:
                leveys = int(leveys)
                korkeus = int(korkeus)
                miinamaara = int(miinamaara) + 1
            except ValueError:
                print "Koitapas uusiksi, muodossa LEVEYS,KORKEUS,MIINAMÄÄRÄ ja ne on ihan kokonaislukuja, leveys ja korkeus keskenään samat."
                continue
            else:
                if 3 <= leveys <= 20 and 3 <= korkeus <= 20 and miinamaara < korkeus * leveys and leveys == korkeus:
                    return leveys, korkeus, miinamaara
                else:
                    print "Laitas nyt järkevämmän kokoinen kartta, leveys ja korkeus samoiksi ja miinoja niin että ne mahtuvat siihen."
                    continue  
 
def luo_kentta(leveys, korkeus, koordinaatit, miinamaara):
    """Luo kentän."""
    kentta = [["0" for i in range(leveys)] for j in range(korkeus)]
    miinat = miinoita_kentta(kentta, koordinaatit, miinamaara)
    miinanumerot(kentta)
    return (kentta, miinat)
 
def nayta_kentta(kentta):
    """Näyttää kentän käyttäjäystävällisemmässä muodossa"""
    for i, j in enumerate(kentta):
        print " | ".join(map(str, j))
   
def miinoita_satunnainen(kentta):
    """Valitsee satunnaiset koordinaatit kentän sisältä."""
    x = random.randint(0, leveys-1)
    y = random.randint(0, korkeus-1)
    return (x, y)
 
def etsi_ymparoivat(kentta, rivin, saraken):
    """Etsii ruutua ympäröivien ruutujen numerot tai miinamäärät."""
    rivi = kentta[rivin]
    sarake = kentta[rivin][saraken]
    ymparoivat = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < rivin + i < leveys and -1 < saraken + j < korkeus and rivin + i != "x" and saraken + j != "x":
                ymparoivat.append((rivin + i, saraken + j))
    return ymparoivat
 
def miinoita_kentta(kentta, koordinaatit, miinamaara):
    """Lisää miinoita_satunnaisesta saatujen koorinaattiarvojen tilalle miinoja."""
    miinat = []
    for i in range(miinamaara):
        ruutu = miinoita_satunnainen(kentta)
        while ruutu == (koordinaatit[0], koordinaatit[1]):
            ruutu = miinoita_satunnainen(kentta)
        miinat.append(ruutu)
    for i, j in miinat:
        kentta[j][i] = "x"
    return miinat
 
def miinanumerot(kentta):
    """Etsii ei-miinaruutujen ympäröivien miinojen määrät."""
    for rivin, rivi in enumerate(kentta):
        for saraken, sarake in enumerate(rivi):
            if sarake != "x":
                arvot = [kentta[c][r] for c, r in etsi_ymparoivat(kentta, rivin, saraken)]
                kentta[rivin][saraken] = str(arvot.count("x"))
 
def nayta_ruudut(kentta, pelikentta, rivin, saraken):
    """Näyttää pelaajan valitseman ruudun ja jos ruutu on 0-ruutu eli yhtään miinaa ympärillä se tekee floodfillin eli näyttää
   numeroruutuja niin kauan että saavutetaan kentän rajat tulee vastaan miinaa ympäröiviä ruutuja."""
    if pelikentta[saraken][rivin] != " ":
        return
    pelikentta[saraken][rivin] = kentta[saraken][rivin]
    if kentta[saraken][rivin] == "0":
        for r, c in etsi_ymparoivat(kentta, rivin, saraken):
            nayta_ruudut(kentta, pelikentta, r, c)
     
def keraa_tilastot(miinamaara, leveys, korkeus, tila, alkuaika, kesto, kierros):
    """Kerää ja kirjoittaa tilastot loppuun asti pelatuista (voitetuista tai hävityistä) peleistä."""
    if tila == "havio":
        lopputulos = "häviö"
    if tila == "voitto":
        lopputulos = "voitto"    
    teksti = ("%s pelatun pelin lopputulos oli %s. Peli kesti %.4f minuutia ja %s kierrosta. Kentän miinamäärä oli %s, sen korkeus %s ja leveys %s. \n") % (alkuaika, lopputulos, kesto, kierros, miinamaara, leveys, korkeus)
    tiedosto = open("tilastot.txt", "a")
    tiedosto.write(teksti)
    tiedosto.close()
   
def voitto_testaus(voittokentta):
    """Luo uuden listan josta poistetaan miinat eli x:ät, näin nähdään onko pelaajan ratkaisema kartta sama kuin kentän kaikki numeroruudut."""
    voittokentta = [[x.replace("x", " ") for x in l] for l in voittokentta]
    return voittokentta
 
def pelaa_pelia():
    """Pääfunktio joka suorittaa pelin pelaamisen. Katsoin apua pelin keston mittaamiseen Stack owerflow'ssa olevasta kysymyksestä: http://stackoverflow.com/questions/13897246/python-time-subtraction"""
    leveys, korkeus, miinamaara = kysy_kentan_muoto()
    pelikentta = [[" " for i in range(leveys)] for i in range(korkeus)]
    nayta_kentta(pelikentta)
    kentta = []
    alkutime = datetime.datetime.now()
    alkuaika = alkutime.strftime('%d/%m/%Y %H:%M:%S')
    kierros = 0
    kesto_alku = datetime.datetime.now()
    ohjeviesti = "Anna koordinaatit jotka haluat arvata muodossa \"x,y\".."
    print "Miinojen määrä on %s. \n" % (miinamaara)
    while True:
        while True:
            koordinaatit = str(raw_input("\n Anna koordinaatit jotka haluat arvata muodossa \"x,y\": ")).split(",")
            print "\n \n"
 
            try:
                koordinaatit = (int(koordinaatit[0]) -1, int(koordinaatit[1]) -1)
            except (IndexError, ValueError):    
                print "Tarkistapas syötteesi, olisi kiva antaa myös ne koordinaatit muodossa jossa ne on pyydetty."
                continue
            else:
                if 0 <= koordinaatit[0] <= (leveys - 1)  and 0 <= koordinaatit[1] <= (korkeus - 1):
                    break
                else:
                    print "olisi kiva osua karttaankin."
 
        if len(kentta) == 0:
            kentta, miinat = luo_kentta(leveys, korkeus, koordinaatit, miinamaara)
        rivin, saraken = koordinaatit
 
        try:
            if kentta[saraken][rivin] == "x":
                print "Hävisit pelin! Parempi onni (taito) ensi kerralla! 8( \n"
                nayta_kentta(kentta)
                kesto = datetime.datetime.now() - kesto_alku
                minuuttikesto = float(kesto.total_seconds() / 60)
                keraa_tilastot(miinamaara, leveys, korkeus, "havio", alkuaika, minuuttikesto, kierros + 1)
                break
            else:
                nayta_ruudut(kentta, pelikentta, rivin, saraken)
                kierros = kierros + 1
        except (IndexError):
            "Vääränlainen syöte." + ohjeviesti
       
        if voitto_testaus(kentta) == voitto_testaus(pelikentta):
            print "Voitit pelin! 8) \n"
            nayta_kentta(kentta)
            kesto = datetime.datetime.now() - kesto_alku
            minuuttikesto = float(kesto.total_seconds() / 60)
            keraa_tilastot(miinamaara, leveys, korkeus, "voitto", alkuaika, minuuttikesto, kierros)
            break
        nayta_kentta(pelikentta)
        jatkosyote = raw_input("\n Anna \"L\" lopettaaksesi peli tai mikä tahansa muu jatkaaksesi: ").lower()
        if jatkosyote == "l":
            break
        else:
            continue