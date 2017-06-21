import RPi.GPIO as GPIO
import os
from time import time, sleep
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

######################Axelle Jamous 2EA1#########################

##############################setup##############################
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ledPin = 18
GPIO.setup(ledPin, GPIO.OUT)

BTN = 17
LED = GPIO.PWM(ledPin, 100) #create object red for PWM on port 12 at 100 Hertz  

GPIO.setup(BTN, GPIO.IN)

LED.start(0) #start LED on 0 percent duty cycle (off)

##############################declarations##############################
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

personCount = 0
send_msg = "dontsend" #at the moment we have to manually toggle send as no instructions were provided this is purely for testing purposes

#MQTT
Broker = "172.16.160.180" #my current IP
snd_topic = "examen" #publish messages to this topic
rcv_topic = "examen" #sub to messages on this topic

##############################MQTT functions##############################
#when connecting:
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))
    mqttc.subscribe(rcv_topic) #sub

#when receving a message:
def on_message(mqttc, obj, msg):
    print("subscribing.")
    try:
        p = msg.payload.decode("utf-8")
        print("decoded payload: " + p)

        x = json.loads(p)
        handleIncomingValues(tuple(x['persons']))
        return
    except Exception as e:
        print(e)

#when subscribing:
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def snd_mqtt(state, dist, trigg):
    lines = readFile("persons.txt")
    count = lines[0]
    dataToSend=json.dumps({"persons":[count,snd_msg]})
    print("sending data through mqtt: " + dataToSend)
    mqttc.publish(snd_topic, dataToSend)

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.connect(Broker, 1883, 60)
mqttc.loop_start() #or client.loop_forever()

##############################functions##############################
def readFile(fileName):
    #read file line per line w timestamps
    f = open(os.path.join(__location__, fileName), "r")
    lines = f.readlines() #list
    f.close()
    return lines

def writeFile(fileName, stringToFile):
    f = open(os.path.join(__location__, fileName), "w")
    f.write(stringToFile)
    f.close()  

def timerCallback(self):
    global personCount

    start_time = time()

    while GPIO.input(self) == 0: # Wait for the button up
        pass

    buttonTime = time() - start_time    # How long was the button down?
    print(str(buttonTime))

    if buttonTime >= 5:
        personsToFile()
        snd_mqtt()
    else:
        personCount += 1
        print("Person count went up: " + str(personCount))

def personsToFile():
    writeFile("persons.txt", str(personCount))

def handleIncomingValues(arrPerson):
    print("Persons received on topic exam: " + arrPerson[0])

    if arrPerson[1] == "send":
        snd_mqtt()

def main():
    LED.ChangeDutyCycle((personCount%10)*10)
    sleep(0.02)

##############################listeners/interrupts##############################
GPIO.add_event_detect(BTN, GPIO.FALLING, callback=timerCallback, bouncetime=500)

##############################toplevel script##############################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            LED.stop()
            GPIO.cleanup()
