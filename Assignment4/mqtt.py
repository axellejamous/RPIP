import RPi.GPIO as GPIO
import os
from time import sleep

btn1 = 5 #red
btn2 = 3 #yellow
led1 = 3 #red
led2 = 3 #yellow
btnMaster = 10 #green

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn1, GPIO.IN)
GPIO.setup(btn2, GPIO.IN)
GPIO.setup(btnMaster, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

#toplevel script
#below will only execute if ran directly - above is always accessible
if __name__ == '__main__':
    while True:
        main()
