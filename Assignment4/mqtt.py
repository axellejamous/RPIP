import RPi.GPIO as GPIO
import os
import io
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

############### gpio in/outputs ##################

btn1 = 3 #red
btn2 = 5 #yellow
btnMaster = 7 #green
led1 = 8 #red
led2 = 10 #yellow
leds = (led1, led2)
led1State = led2State = false;

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn1, GPIO.IN)
GPIO.setup(btn2, GPIO.IN)
GPIO.setup(btnMaster, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

############### MQTT section ##################

Broker = "192.168.1.10"

rcv_topic = "home/groundfloor/livingroom/lights/lightx"    # receive messages on this topic
snd_topic = "home/groundfloor/kitchen/lights/lightx"       # send messages to this topic

#when connecting:
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))
    mqttc.subscribe(rcv_topic) #receving/subscriber

#when receving a message:
def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    try:
        p = msg.payload.decode("utf-8")
        print(p)
        x = json.loads(p)
        set_leds(leds, tuple(x['leds'])) #set leds to received value

        return
    except Exception as e:
        print(e)

# callback functie voor publish  event
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

# callback functie voor subscribe event
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

mqttc = mqtt.Client()
mqttc.connect(Broker, 1883, 60) #last could be a port too
mqttc.loop_start() #client.loop_forever()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

############### led&button related ##################

def set_leds(leds, states):
    GPIO.output(leds, states)  #Turn OFF LED

def snd_msg(led):
    global led1State
    global led2State

    if led==1:
        led1State = not led1State
    elif led==2:
        led2State = not led2State
    elif led==3:
        led1State = led2State = false
    else:
        print('mate the wrong parameter is being given')

    dataToSend = {"leds":[led1State,led2State]}
    mqttc.publish(snd_topic, dataToSend)

io.add_event_detect(btn1,io.FALLING,callback=snd_msg(1),bouncetime=500)
io.add_event_detect(btn2,io.FALLING,callback=snd_msg(2),bouncetime=500)
io.add_event_detect(btnMaster,io.FALLING,callback=snd_msg(3),bouncetime=500)

############### main ##################

def main():
    try:
        while True:
            dataToSend = "tmp";
            mqttc.publish(snd_topic, str(dataToSend))
            sleep(1*60)
            #mqttc.loop() #ASK TEACHER
    except KeyboardInterrupt:
        pass
    finally:
#        io.cleanup()

#toplevel script
#below will only execute if ran directly - above is always accessible
if __name__ == '__main__':
    main()
