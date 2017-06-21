import RPi.GPIO as GPIO
import os
from time import strftime, time, sleep
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

######################Axelle Jamous 2EA1#########################

##############################setup##############################
BTN = 11
LED = 12 #pwm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

##############################declarations##############################
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

personCount = 0

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
        showPersons(tuple(x['persons']))
        return
    except Exception as e:
        print(e)

#when subscribing:
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def snd_mqtt(state, dist, trigg):
    dataToSend=json.dumps({"persons":[personCount]})
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

def appendFile(fileName, stringToFile):
    f = open(os.path.join(__location__, fileName), "a")
    f.write(stringToFile)
    f.close()

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
        personCount++

def personsToFile():
    appendFile("persons.txt", str(personCount))

def showPersons(arrPerson):
    print("Persons received on topic exam: " + arrPerson[0])

def main():
    return

##############################listeners/interrupts##############################
GPIO.add_event_detect(BTN, GPIO.FALLING, callback=timerCallback, bouncetime=500)

##############################toplevel script##############################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            GPIO.cleanup()
