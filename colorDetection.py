import numpy as np
import cv2 as cv
import mouvement as mv


DIST_MAX: int = 100
HUE_MAX: int = 25
ROTATION_AMOUNT: int = 5
HORS_ECRAN: int = 10000 # valeur supérieur à la largeur de l'écran 
CAP = cv.VideoCapture(1)
CAP.set(cv.CAP_PROP_FRAME_WIDTH, 320)
CAP.set(cv.CAP_PROP_FRAME_HEIGHT, 240)


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
                # lost = True
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
    binaryMap, centroid = getObjectMap(hue)
    if centroid is None:
        return HORS_ECRAN

    width = binaryMap.shape[1]
    cx, _ = centroid
    # offset par rapport au centre (>0 = à droite, <0 = à gauche)
    return int(cx - (width // 2))

def getObjectMap(hue: int): # image opencv
    ret, frame = CAP.read()
    if not ret or frame is None:
        print("error lecture")
        return np.zeros((240, 320), dtype=np.uint8), None

    # s'assurer de la taille attendue
    frame = cv.resize(frame, (320, 240))

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # calculer lower/upper en modulo sur 0-179 (OpenCV hue range)
    lower = int((hue - HUE_MAX) % 180)
    upper = int((hue + HUE_MAX) % 180)

    # si pas de wrap-around -> une seule plage, sinon deux plages à combiner
    if lower <= upper:
        mask = cv.inRange(hsv, np.array([lower, 60, 60]), np.array([upper, 255, 255]))
    else:
        mask1 = cv.inRange(hsv, np.array([lower, 60, 60]), np.array([179, 255, 255]))
        mask2 = cv.inRange(hsv, np.array([0, 60, 60]), np.array([upper, 255, 255]))
        mask = mask1 | mask2

    # nettoyage rapide
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    binaryMap = np.zeros(mask.shape, dtype=np.uint8)
    centroid = None

    if contours:
        c = max(contours, key=cv.contourArea)
        if cv.contourArea(c) > 100:  # seuil pour ignorer le bruit
            cv.drawContours(binaryMap, [c], -1, 255, -1)
            M = cv.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centroid = (cx, cy)

    cv.imshow("Camera Feed", binaryMap)
    return binaryMap, centroid