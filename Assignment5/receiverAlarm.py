import os
import slacker as slack
from time import strftime, sleep
from gpiozero import LED, Button
import json

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

######################setup#########################
toggleBtn = Button(2)
distanceBtn = Button(3)
holdBtn = Button(4, hold_time=5)
led = LED(14)
ledS = LED(15)

#################global declarations##################
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
ledState = alarmState = distance = 0
toggleState = False
timerState = True

############### MQTT section ##################
Broker = "192.168.1.118"

snd_topic = "home/receiver" #sub to messages on this topic
rcv_topic = "home/alarmer" #publish messages to this topic

#when connecting:
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))
    mqttc.subscribe(rcv_topic) #sub

#when receving a message:
def on_message(mqttc, obj, msg):
    print("subscribing.")
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    try:
        p = msg.payload.decode("utf-8")
        print("decoded payload: " + p)

        x = json.loads(p)
        handle_values(tuple(x['values']))
        return
    except Exception as e:
        print(e)

#when subscribing:
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

############### assign functions to mqtt ###############
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.connect(Broker, 1883, 60)
mqttc.loop_start() #or client.loop_forever()

def snd_msg(buttonHeld, toggle):
    dataToSend=json.dumps({"values":[buttonHeld,toggle]})
    print("sending data through mqtt: " + dataToSend)
    mqttc.publish(snd_topic, dataToSend)

####################functions#########################
def handle_values(values):
    global alarmState, distance, timerState

    alarmState = values[0]
    distance = values[1]

    if values[2]: #True
        firstTrigger()

    #alarm was retriggered
    timerState = False #so timerbtn untriggered


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
    appendFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S"))) #output time to file
    slack.send_msg('#pi','Alarm was triggered.') #send slack msg

def timer():
    global timerState

    timerState = True
    #send this through mqtt
    snd_msg(timerState, toggleState)

def toggler():
    global toggleState

    toggleState = not toggleState
    #send changed alarm state through mqtt
    snd_msg(timerState, toggleState)

def showDistance():
    print("distance: " + str(distance))

def alarm():
    global ledState

    if alarmState == 1 and not timerState: #ALARM ON
        ledState = not ledState
        led.value = ledState #turn on or off led depending on state
        ledS.on()

    elif alarmState == 0 or timerState: #ALARM OFF
        ledState = False
        led.off()
        ledS.off()

def main():
    alarm()
    sleep(0.2)

###################interrupts#######################
holdBtn.when_held = timer
toggleBtn.when_pressed = toggler
distanceBtn.when_pressed = showDistance

#################toplevel script####################
if __name__ == '__main__':
    while True:
        main()
