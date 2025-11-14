import numpy as np
import cv2 as cv
import mouvement as mv


DIST_MAX: int = 100
HUE_MAX: int = 25
ROTATION_AMOUNT: int = 5
HORS_ECRAN: int = 10000 # valeur supérieur à la largeur de l'écran 
CAP = cv.VideoCapture(0)


# permet d'aller a un objet de couleurs dont on donne le hue
# TODO: Vérifier l'intéret de plus de précision de couleur avec un hsv ou rgb complet
def goTo(hue: int) -> None:
    toClose = False
    lost = False
    while(not(toClose or lost)):
        cibleDirection = getCibleDirection(hue)
        # TODO: Verifier la distance de l'objet ne question pour toClose et pouvoir recentré le robot en "1 image"
        if(cibleDirection in range(-DIST_MAX, DIST_MAX)):
            # La cible est dans la distance de décalage accepter on peut avancer
            mv.forward(5)
            pass
        elif(cibleDirection != HORS_ECRAN):
            # La cible est hors de la distance de décalage mais dans l'écran on peut donc utilisé cibleDirection pour recentré le robot
            
            pass
        else:
            # la cible est hors de l'écran on doit donc faire tourner le robot sur lui meme jusqu'a ce qu'il la retrouve
            if(not(searchCible(hue))): 
                lost = True
                # Error: cible perdue passage à l'operation suivante
            pass
        cv.waitKey(1)  # Minimum pour le traitement des événements

 
# fait faire un tour sur lui meme haut robot il s'arrete quand il aligne la cible au centre de l'écran il renvoie true si il la trouve false si il fait un tour complet sans succes
def searchCible(hue: int) -> bool:
    rotation = 0
    while(getCibleDirection(hue) == HORS_ECRAN):
        if(rotation >= 360):
            return False
        mv.turn(5)
        rotation += 5
    return True

        
# donne l'emplacement de la cible pour la camera 
def getCibleDirection(hue: int) -> int:
    res, binaryMap = getObjectMap(hue)
    if not res:
        return HORS_ECRAN
    
    # retourne les coordonnée x du centre de l'objet
    return 0


def getObjectMap(hue: int): # image opencv
    ret, frame = CAP.read()
    if(not(ret)):
        print("error lecture")
   
   # TODO
   # convertit en HSV
   # créer un masque selon le hue
   # trouver les contour
   # Si contour sélectioner le plus gros
   # créer une image binaire de l'objet l'afficher et la retourner
    
    contours = 0
    binaryMap = 0
    
    cv.imshow("Camera Feed", frame)
    return contours, binaryMap