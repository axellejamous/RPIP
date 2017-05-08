import RPi.GPIO as GPIO
import os
from time import sleep, strftime, time

IRS = 11
BTN = 5
LED = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IRS, GPIO.IN) #Read output from IR motion sensor
GPIO.setup(BTN, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

globFlag = 0

def cleanupTool():
    lineCln()
    rangeCln()
    return

def lineCln():
    lines = readFile("logFile.txt")  
    #print every line and ask user if he wants to delete it 
    return

def rangeCln():
    lines = readFile("logFile.txt")
    #ask user for start and stop date
    #delete all entries in file in given date range
    return

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
        print(elapsed)

    #GPIO.add_event_detect(channel, GPIO.RISING)  # add rising edge detection on a channel
    #    do_something()
    #if GPIO.event_detected(channel):
    #    print('Button pressed')

# only add the detection call once!
GPIO.add_event_detect(BTN, GPIO.BOTH, callback=timerCallback) 

def main():
    global globFlag
    
    i=GPIO.input(IRS)
    if i==0:                 #When output from motion sensor is LOW
        #set flag back to 0 for time
        globFlag = 0
        
        print "Door closed",i
        GPIO.output(LED, 0)  #Turn OFF LED
        sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        if globFlag==0:
            #output time to file
            writeFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S")))
            #set flag to on
            globFlag = 1

        #door is still open but hasn't been shut    
        print "Door open",i
        GPIO.output(LED, 1)  #Turn ON LED
        sleep(0.1)

#toplevel script
#below will only execute if ran directly - above is always accessible 
if __name__ == '__main__':
    while True:
        main()
