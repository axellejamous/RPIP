import RPi.GPIO as GPIO
from time import sleep, strftime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from IR motion sensor
GPIO.setup(2, GPIO.IN)          #Button
GPIO.setup(3, GPIO.OUT)         #LED output pin

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
    f.close

def main():
    global globFlag
    
    i=GPIO.input(11)
    if i==0:                 #When output from motion sensor is LOW
        #set flag back to 0 for time
        globFlag = 0
        
        print "No intruders",i
        GPIO.output(3, 0)  #Turn OFF LED
        sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        if globFlag==0:
            #output time to file
            writeFile("timeFile.txt", time.strftime("%a, %d %b %Y %H:%M:%S"))
            #set flag to on
            globFlag = 1

        #door is still open but hasn't been shut    
        print "Intruder detected",i
        GPIO.output(3, 1)  #Turn ON LED
        sleep(0.1)


#toplevel script
#below will only execute if ran directly - above is always accessible 
if __name__ == '__main__':
    while True:
        main()
