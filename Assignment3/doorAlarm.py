import RPi.GPIO as GPIO
import os
from time import strftime, time

######################Axelle Jamous 2EA1#########################

##############################setup##############################
IRS = 11
BTN = 5
LED = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IRS, GPIO.IN) #Read output from IR motion sensor
GPIO.setup(BTN, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

##############################declarations##############################
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

fileFlag = 0
alarmState = 0
ledState = False
previousTime = 0

##############################functions##############################
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

def timeToFile():
    #writes the time that the alarm was triggered to a timeFile.txt
    global fileFlag

    if fileFlag==0:
        fileFlag = 1 #tell the program that the first time has passed
        appendFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S"))) #output time to file

def alarm():
    global alarmState, ledState

    if alarmState == 1: #alarm on
        ledState = not ledState
    elif alarmState == 0: #alarm off
        ledState = False

    GPIO.output(LED, ledState) #write change to led

def timerCallback(self):
    global alarmState
    global previousTime

    ontime = time.time() - previousTime
    if ontime > 1 and ontime < 3:
        alarmState = 1
        print("hold")
    elif ontime > 3:
        alarmState = 0
        print("long hold")
    elif ontime > 0.01:
        alarmState = 1
        print("click")
    else:
        print("ignore")

def main():
    global fileFlag, alarmState, previousTime

    previousTime = time.time()

    i=GPIO.input(IRS) #read infrared sensor output
    if i==0:
        fileFlag = 0
        alarmState = 0
#       print("Door closed " + str(i))

    elif i==1:
        timeToFile()
        alarmState = 1
#       print("Door open " + str(i))

    alarm()

##############################listeners/interrupts##############################
GPIO.add_event_detect(BTN, GPIO.BOTH, callback=timerCallback, bouncetime=200)


##############################toplevel script##############################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            GPIO.cleanup()
