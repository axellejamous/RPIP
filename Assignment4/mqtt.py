import RPi.GPIO as GPIO
import os
from time import sleep
import paho.mqtt.client as mqtt

btn1 = 5 #red
btn2 = 3 #yellow
led1 = 3 #red
led2 = 3 #yellow
btnMaster = 10 #green

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn1, GPIO.IN)
GPIO.setup(btn2, GPIO.IN)
GPIO.setup(btnMaster, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

# aanmaken van mqtt client object
mqttc = mqtt.Client()

# toewijzen van callback functies
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

#connect and subscribe
mqttc.connect("127.0.0.1")
mqttc.subscribe("home/groundfloor/livingroom/lights/lightx")

def set_leds(leds, states):
    io.output(leds, states)

# callback functie voor connect event
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

# callback functie voor message event
def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    try:
        # payload omzetten van bytestring naar string
        p = msg.payload.decode("utf-8")

        # json wordt verwacht json string moet omgezet worden naar een python
        #  dictonary voor verwerking
        x = json.loads(p)

        #
        set_leds(leds, tuple(x['leds']))
        return
    except Exception as e:
        print(e)

# callback functie voor publish  event
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

# callback functie voor subscribe event
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def main():
    try:
        while True:
            mqttc.loop()
    except KeyboardInterrupt:
        pass
    finally:
        io.cleanup()

#toplevel script
#below will only execute if ran directly - above is always accessible
if __name__ == '__main__':
    main()
