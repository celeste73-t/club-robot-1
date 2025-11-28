# library de gestion des moteur
import RPi.GPIO as GPIO
import time

AIN1 = 26
AIN2 = 20
PWMA = 21
STBY = 22
BIN1 = 17
BIN2 = 27
PWMB = 18

TEMPS360 = 4 # remplacer par le vrai temps 360

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)

FORCE = 40

# Deux PWM séparés
pwmA = GPIO.PWM(PWMA, 1000)
pwmB = GPIO.PWM(PWMB, 1000)

pwmA.start(0)
pwmB.start(0)

# Activer le driver
GPIO.output(STBY, GPIO.HIGH)
def forward(timer: int) -> None:
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(FORCE)
    pwmB.ChangeDutyCycle(FORCE)
    time.sleep(timer)

    
def backward(timer: int) -> None:
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(FORCE)
    pwmB.ChangeDutyCycle(FORCE)
    time.sleep(timer)
    print("le robot recul de " + str(timer))
    
def turn(degree: int) -> None:
    duration = abs(degree) / 360 * TEMPS360
    
    if(degree>0 ):
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
    else:
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(FORCE)
    pwmB.ChangeDutyCycle(FORCE)
    time.sleep(duration)

    print("le robot tourne de " + str(degree) + "degrées")

turn(1)
turn(-2)
forward(1)
backward(3)
