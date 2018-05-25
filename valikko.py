#-*- coding: utf-8 -*-    
#2014
#Suorita tämä tiedosto käynnistääksesi peli/tilastot.
 
import miinantallaaja
 
while True:
    print "\n Miinaharava Deluxe edition \n valitse mitä haluat tehdä \n p - pelaa Miinaharava Deluxe editionia \n t - katsele tilastoja \n l - lopeta pelaaminen"
    valikkosyote = raw_input("").lower()
    if valikkosyote == "p":
        """Aloittaa pelin."""
        miinantallaaja.pelaa_pelia()
        continue
    if valikkosyote == "t":
        """Näyttää tilastot jos niitä on, mahdollisuus tyhjentää tilastot."""
        try:
            tiedosto = open("tilastot.txt", "r")
        except IOError:
            print "Ei tilastoja :(. Pelaa ensin!"
            continue
        else:
            lue = tiedosto.read()
            tiedosto.close()
            print "Tilastot: \n\n" + lue
            syote = raw_input("Syötä t tyhjentääksesi pelihistoria tai mitä tahansa muuta poistuaksesi päävalikkoon.")
            if syote == "t":
                tyhjennys = open("tilastot.txt", "w")
                tyhjennys.write("")
                tyhjennys.close()
                print "Pelihistoria tyhjennetty."
                continue
            else:
                continue
    if valikkosyote == "l":
        """Lopettaa pelin."""
        print "Kiitos pelaamisesta, tervetuloa takaisin!"
        break
    else:
        print "Nyt et kyllä ilmaissut kovin selkeästi mitä haluat tehdä, luepa uudestaan miten voit suorittaa minkäkin toiminnon."
        continue
