import RPi.GPIO as GPIO
import os
from time import sleep, strftime, time, strptime

IRS = 11
BTN = 5
LED = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IRS, GPIO.IN) #Read output from IR motion sensor
GPIO.setup(BTN, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#global
globFlag = 0
globLedState = False
globBtnState = 0
start = end = 0

def readFile(fileName):
    #read file line per line w timestamps
    f = open(os.path.join(__location__, fileName), "r")
    lines = f.readlines() #list
    f.close()
    return lines

def appendFile(fileName, stringToFile):
    f = open(os.path.join(__location__, fileName), "a")
    f.write(stringToFile)
    f.close()

def writeFile(fileName, stringToFile):
    f = open(os.path.join(__location__, fileName), "w")
    f.write(stringToFile)
    f.close()

def timerCallback(self):
    global start
    global end
    global globBtnState

    if GPIO.input(BTN) == 1:
        start = time()
    if GPIO.input(BTN) == 0:
        end = time()
        elapsed = end - start
        #print(elapsed)

    if elapsed<5:
        globBtnState = 0
    elif elapsed>=5:
        globBtnState = 1
        print("Button pressed longer than 5s - alarm off")

GPIO.add_event_detect(BTN, GPIO.BOTH, callback=timerCallback, bouncetime=200)

def main():
    global globFlag
    global globLedState
    global globBtnState

    i=GPIO.input(IRS)
    if i==0:                 #When output from motion sensor is LOW
        #set flag back to 0 for time
        globFlag = 0
        globLedState = False
        #reset alarmled
        globBtnState = 0
        print("Door closed " + str(i))
        GPIO.output(LED, globLedState)  #Turn OFF LED
        sleep(0.1)
    #alarm on:
    elif i==1:               #When output from motion sensor is HIGH
        print("Door open " + str(i))

        #first time alarm starts going off
        if globFlag==0:
            #output time to file
            appendFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S")))
            #set flag to on
            globFlag = 1

        if globBtnState == 0:
            globLedState = not globLedState
            GPIO.output(LED, globLedState)  #Turn ON LED
        elif globBtnState == 1:
            globLedState = False
            GPIO.output(LED, globLedState)  #Turn ON LED

#toplevel script
#below will only execute if ran directly - above is always accessible
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            GPIO.cleanup()
