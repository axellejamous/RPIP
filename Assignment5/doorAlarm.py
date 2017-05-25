import os
from time import sleep, strftime, time, strptime
from gpiozero import DistanceSensor, LED, Button

######################setup#########################
toggleBtn = Button(2)
distanceBtn = Button(3)
holdBtn = Button(4, hold_time=5)
led = LED(14)
ultrasonic = DistanceSensor(echo=17, trigger=18) #threshold is set to 0.3m standard
# LED WAS 3
# TRIGGER WAS 4

#################global declarations##################
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fileFlag = holdState = 0
ledState = False

####################functions#########################
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

def writeto_file():
    #first time alarm starts going off, write to file:
    if fileFlag==0:
        #output time to file
        appendFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S")))
        #set flag to on
        fileFlag = 1

def alarmer():
    if holdState == 0:
        ledState = not ledState
        led.value = ledState #turn on or off led depending on state

def timer():
    global holdState, ledState
    led.off
    ledState = False
    holdState = 1 #so that it doesn't get triggered in main anymore

def toggler():
    global holdState
    holdState = 0
    alarmer()

def showDistance():
    print("distance: " + str(ultrasonic.distance))

###################interrupts#######################
holdBtn.when_held = timer
toggleBtn.when_pressed = toggler
distanceBtn.when_pressed = showDistance

#####################main###########################
def main():
    global fileFlag, ledState, holdState

    #alarm off:
    ultrasonic.wait_for_out_of_range()
        print("Door closed")

        led.off #Turn OFF led

        fileFlag = holdState = 0 #reset button press so that the alarm goes off again & file write
        ledState = False #reset alarmled

    #alarm on:
    ultrasonic.wait_for_in_range()
        print("Door open")

        writeto_file()
        alarmer()


#################toplevel script####################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            #CLEANUP IS AUTOMATIC WITH GPIOZERO
