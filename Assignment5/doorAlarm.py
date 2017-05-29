from time import sleep
from gpiozero import DistanceSensor, LED

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

######################setup#########################
led = LED(14)
ledS = LED(15)
ultrasonic = DistanceSensor(echo=17, trigger=4) #threshold is set to 0.3m standard
# LED WAS 3
# TRIGGER WAS 4

#################global declarations##################
triggerFlag = buttonFlag = alarmState = 0
ledState = toggleFlag = False

valueList = None

############### MQTT section ##################
Broker = "172.16.175.235"

snd_topic = "home/alarmer" #publish messages to this topic
rcv_topic = "home/receiver" #sub to messages on this topic

#when receving a message:
def on_message(mqttc, obj, msg):
    global alarmState, buttonFlag, toggleFlag

    print("subscribing.")
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    try:
        p = msg.payload.decode("utf-8")
        print("decoded payload: " + p)
        valueList = p.split()

        if valueList[0]: #button hold - True
            alarmState = 0
            buttonFlag = 1

        if valueList[1]: #toggle - True
            toggleFlag = True
        elif not valueList[1]:
        	toggleFlag = False

        return

    except Exception as e:
        print(e)

#when subscribing:
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def snd_msg(state, dist, trigg):
    print("mqtt send message start")
    valueList = [str(state), str(dist), str(trigg)]
    stringVal = ' '.join(valueList)
    print("data: " + stringVal)
    mqttc.publish(snd_topic, stringVal)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.connect(Broker, 1883, 60)
mqttc.loop_start() #or client.loop_forever()

####################functions#########################
def firstTrigger():
    global triggerFlag

    #first time alarm starts going off, write to file:
    if triggerFlag==0:
        print(str(ultrasonic.distance))
        snd_msg(alarmState, str(ultrasonic.distance), True)
        triggerFlag = 1 #first time has passed
        print("first trigger.")

def alarm():
    global ledState

    if alarmState == 1: #ALARM ON
        ledState = not ledState
        led.value = ledState #turn on or off led depending on state
        ledS.on

    elif alarmState == 0: #ALARM OFF
        ledState = False
        led.off
        ledS.off

def outOfRange():
    global triggerFlag, buttonFlag, alarmState

    print("Door closed")
    triggerFlag = buttonFlag = 0 #reset file, toggle and button flags
    alarmState = 0 #alarm is off

def inRange():
    global alarmState

    print("Door open")
    firstTrigger()
    if buttonFlag == 0:
        alarmState = 1
        print("alarm state changed to 1.")

#####################main###########################
def main():

    ultrasonic.when_out_of_range = outOfRange()
    ultrasonic.when_in_range = inRange()

    print("starting alarm")
    alarm()
    snd_msg(alarmState, str(ultrasonic.distance), False)
    sleep(0.2)

def mainToggle():
	global alarmState

	alarmState = not alarmState
	alarm()
	sleep(0.2)

#################toplevel script####################
if __name__ == '__main__':
    while True:
        if toggleFlag:
        	mainToggle()
        elif not toggleFlag:
            main()
