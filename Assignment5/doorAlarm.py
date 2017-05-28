import os
from time import strftime, sleep
from gpiozero import DistanceSensor, LED, Button

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

######################setup#########################
led = LED(14)
ledS = LED(15)
ultrasonic = DistanceSensor(echo=17, trigger=18) #threshold is set to 0.3m standard
# LED WAS 3
# TRIGGER WAS 4

#################global declarations##################
triggerFlag = buttonFlag = toggleFlag = alarmState = 0
ledState = False

valueList = None

############### MQTT section ##################
Broker = "192.168.1.10"

snd_topic = "home/alarmer" #publish messages to this topic
rcv_topic = "home/receiver" #sub to messages on this topic

#when receving a message:
def on_message(mqttc, obj, msg):
    global alarmState, buttonFlag

    print("subscribing.")
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    try:
        p = msg.payload.decode("utf-8")
        print("decoded payload: " + p)
        valueList = p.split()

        if valueList[0]: #True
            alarmState = 0
            buttonFlag = 1

        if valueList[1]: #True
            alarmState = not alarmState #toggle
            toggleFlag = 1
        return

    except Exception as e:
        print(e)

#when subscribing:
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

############### assign functions to mqtt ###############
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.connect(Broker, 1883, 60)
mqttc.loop_start() #or client.loop_forever()

def snd_msg(state, dist, trigg):
    #if data is being sent, that means alarmstate is on!!!
    #dataToSend=json.dumps({"state":[alarmState], , "dist":[distance]})
    valueList = [state, dist, trigg]
    stringVal = ' '.join(valueList)
    print("data: " + stringVal)
    mqttc.publish(snd_topic, stringVal)

####################functions#########################
def firstTrigger():
    #first time alarm starts going off, write to file:
    if triggerFlag==0:
        #send signal to trigger firsttrigger on pi2
        snd_msg(alarmState, str(ultrasonic.distance), True)
        triggerFlag = 1 #first time has passed

def alarm():
    global ledState

    if alarmState == 1: #ALARM ON
        ledState = not ledState
        led.value = ledState #turn on or off led depending on state
        ledS.on

    else if alarmState == 0: #ALARM OFF
        ledState = False
        led.off
        ledS.off

#####################main###########################
def main():
    global triggerFlag, alarmState, buttonFlag

    ultrasonic.wait_for_out_of_range()
        print("Door closed")
        triggerFlag = buttonFlag = 0 #reset file and button flags
        alarmState = 0 #alarm is off

    ultrasonic.wait_for_in_range()
        print("Door open")
        firstTrigger()
        if buttonFlag == 0 and toggleFlag == 0:
            alarmState = 1

    alarm()
    snd_msg(alarmState, str(ultrasonic.distance), False)
    sleep(0.2)

#################toplevel script####################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            #CLEANUP IS AUTOMATIC WITH GPIOZERO
