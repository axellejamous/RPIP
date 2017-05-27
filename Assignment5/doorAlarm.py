import os
from time import strftime
from gpiozero import DistanceSensor, LED, Button
import socket
from slackclient import SlackClient

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
triggerFlag = alarmState = 0
ledState = False

####################slack setup#######################
SLACK_TOKEN = 'insert token here' #deleted my token for github but to test place a token here
slack_client = SlackClient(SLACK_TOKEN)
user_slack_id = '@axelle' #change this to your own username for testing
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80)) #surf to google dns and see what ip it uses
ip = s.getsockname()[0]
s.close()

####################slack functions###################
def send_msg(channel_id, msg):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel_id,
		text=msg,
		username='pythonbot',
		icon_emoji=':robot_face:'
	)

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

def firstTrigger():
    #first time alarm starts going off, write to file:
    if triggerFlag==0:
        appendFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S"))) #output time to file
        send_msg('general','hello') #send slack msg

        triggerFlag = 1 #first time has passed

def alarmer():
    if alarmState == 1: #ALARM ON
        ledState = not ledState
        led.value = ledState #turn on or off led depending on state

    else if alarmState == 0: #ALARM OFF
        ledState = False
        led.off

def timer():
    global alarmState
    alarmState = 0

def toggler():
    global alarmState
    alarmState = not alarmState

def showDistance():
    print("distance: " + str(ultrasonic.distance))

###################interrupts#######################
holdBtn.when_held = timer
toggleBtn.when_pressed = toggler
distanceBtn.when_pressed = showDistance

#####################main###########################
def main():
    global triggerFlag, alarmState

    ultrasonic.wait_for_out_of_range()
        print("Door closed")
        triggerFlag = 0 #reset file flag
        alarmState = 0 #alarm is off

    ultrasonic.wait_for_in_range()
        print("Door open")
        firstTrigger()
        alarmState = 1

    alarmer()

#################toplevel script####################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            #CLEANUP IS AUTOMATIC WITH GPIOZERO
