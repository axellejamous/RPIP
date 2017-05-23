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
start = end = 0

#cleanuptool function to be imported
def cleanupTool():
    #read all lines in the file then close it
    #logFile=open("logFile.txt","r")
    #lines=file.readlines()
    #logFile.close()
    lines = readFile("timeFile.txt")

    #Offer user two modes in which he can cleanup the file
    mode=raw_input("Type 1 to clean up line per line, type 2 to clean up a certain range: ")
    if(mode=="1"):
        print("Cleaning line per line")
        for line in list(lines):
            rm=raw_input("Do you want to remove this line? (y)")
            if(rm=="y"):
                lines.remove(line)
    elif(mode=="2"):
        print("".join(lines))
        startdate=time.strptime(raw_input("Select start date to remove"),"%a, %d %b %Y %H:%M:%S")
        enddate=time.strptime(raw_input("Select end date to remove"),"%a, %d %b %Y %H:%M:%S")
        print("Start: " + startdate + " End: " + enddate)
        for line in list(lines):
            dateLine=strptime(line.rstrip("\n"),"%a, %d %b %Y %H:%M:%S")
            if(startdate<=dateLine<=enddate):
                lines.remove(line)

    #Write changes to the file:
    #logFile=open("logFile.txt","w")
    #logFile.write("".join(lines))
    #logFile.close()
    writeFile("timeFile.txt","".join(lines))

def readFile(fileName):
    #read file line per line w timestamps
    f = open(os.path.join(__location__, fileName), "r")
    lines = f.readlines() #list
    f.close()
    return lines

def writeFile(fileName, stringToFile):
    f = open(os.path.join(__location__, fileName), "a")
    f.write(stringToFile)
    f.close()

def timerCallback():
    global start
    global end
    if GPIO.input(BTN) == 1:
        start = time()
    if GPIO.input(BTN) == 0:
        end = time()
        elapsed = end - start
        #print(elapsed)
    return elapsed

# only add the detection call once!
GPIO.add_event_detect(BTN, GPIO.BOTH)

def main():
    if GPIO.event_detected(BTN):
        elapsed = timerCallback()

    global globFlag
    global globLedState

    i=GPIO.input(IRS)
    if i==0:                 #When output from motion sensor is LOW
        #set flag back to 0 for time
        globFlag = 0
        globLedState = False
        print("Door closed " + i)
        GPIO.output(LED, globLedState)  #Turn OFF LED
        sleep(0.1)
    #alarm on:
    elif i==1:               #When output from motion sensor is HIGH
        print("Door open " + i)

        #first time alarm starts going off
        if globFlag==0:
            #output time to file
            writeFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S")))
            #set flag to on
            globFlag = 1


        if elapsed<5:
            globLedState = not globLedState
            GPIO.output(LED, globLedState)  #Turn ON LED
        elif elapsed >=5:
            globLedState = False
            GPIO.output(LED, globLedState)  #Turn ON LED

        #sleep(0.1)

#toplevel script
#below will only execute if ran directly - above is always accessible
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            GPIO.cleanup()
