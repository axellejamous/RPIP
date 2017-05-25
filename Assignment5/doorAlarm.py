import os
from time import sleep, strftime, time, strptime
from gpiozero import DistanceSensor, LED, Button

###################declarations#######################

button = Button(5, hold_time=5)
led = LED(3)
ultrasonic = DistanceSensor(echo=17, trigger=4) #threshold is set to 0.3m standard

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#global
fileFlag = btnState = 0
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

def timer(self):
    global btnState

    led.off
    btnState = 1 #so that it doesn't get triggered in main anymore


###################interrupts#######################
button.when_held = timer
#button.when_pressed = timer

#####################main###########################
def main():
    global fileFlag, ledState, btnState

    #alarm off:
    ultrasonic.wait_for_out_of_range()
        print("Door closed")

        led.off #Turn OFF led

        fileFlag = 0
        ledState = False #reset alarmled
        btnState = 0 #reset button press so that the alarm goes off again

    #alarm on:
    ultrasonic.wait_for_in_range()
        print("Door open")
        #first time alarm starts going off, write to file:
        if fileFlag==0:
            #output time to file
            appendFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S")))
            #set flag to on
            fileFlag = 1

        if btnState == 0:
            btnState = not btnState
            led.value = ledState #turn on or off led depending on state

#################toplevel script####################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            #CLEANUP IS AUTOMATIC WITH GPIOZERO
