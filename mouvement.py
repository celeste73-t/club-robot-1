# library de gestion des moteur

def forward(amount: int) -> None:
    # utiliser la library de gestion des moteur pour avancer
    print("le robot avance de " + str(amount))
    
def backward(amount: int) -> None:
    # utiliser la library de gestion des moteur pour reculer
    print("le robot recul de " + str(amount))
    
def turn(amount: int) -> None:
    # utiliser la library de gestion des moteur pour tourner
    print("le robot tourne de " + str(amount) + "degrées")