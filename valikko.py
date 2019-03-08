#-*- coding: utf-8 -*-    
# Run this file to play or view the statistics.
 
import miinantallaaja
 
while True:
    print "\n Miinaharava Deluxe edition \n Choose, what you wish to do \n p - play \n s - view statistics \n q - quit"
    valikkosyote = raw_input("").lower()
    if valikkosyote == "p":
        """Begins the game."""
        miinantallaaja.pelaa_pelia()
        continue
    if valikkosyote == "s":
        """Shows statistics, if any, or empties them."""
        try:
            tiedosto = open("tilastot.txt", "r")
        except IOError:
            print "No statistics :(. Play the game first!"
            continue
        else:
            lue = tiedosto.read()
            tiedosto.close()
            print "Tilastot: \n\n" + lue
            syote = raw_input("Input w to wipe out the statistics or anything else to go back.")
            if syote == "w":
                tyhjennys = open("tilastot.txt", "w")
                tyhjennys.write("")
                tyhjennys.close()
                print "Statistics cleared."
                continue
            else:
                continue
    if valikkosyote == "q":
        """Ends the game."""
        print "Thank you for playing!"
        break
    else:
        print "Input not recognized! Please read the prompt message again."
        continue
