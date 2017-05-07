import RPi.GPIO as GPIO
from time import sleep
#from gpiozero import Button, LED

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

#button = Button(3)
#led = LED(2)

def cleanupTool():
    lineCln()
    rangeCln()
    return

def lineCln():
    lines = readFile()
    
    #print every line and ask user if he wants to delete it
    
    return

def rangeCln():
    lines = readFile()

    #ask user for start and stop date
    #delete all entries in file in given date range

    return

def readFile():
    #read file line per line w timestamps
    f = open(logs, r)
    lines = f.readlines() #list
    f.close()
    return lines

def main():
    i=GPIO.input(11)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
        GPIO.output(3, 0)  #Turn OFF LED
        #led.on()
        sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print "Intruder detected",i
        GPIO.output(3, 1)  #Turn ON LED
        #led.off()
        sleep(0.1)
    
    #try:
    #    break
    #except ValueError:
    #    print "Oops!  That was no valid number.  Try again..."
    #return

#toplevel script will only execute if ran directly:
if __name__ == '__main__':
    while True:
        main()
