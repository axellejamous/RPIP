import slacker as slack
from gpiozero import LED, Button

######################setup#########################
toggleBtn = Button(2)
distanceBtn = Button(3)
holdBtn = Button(4, hold_time=5)
led = LED(14)
ledS = LED(15)

#################global declarations##################
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
ledState = alarmState = distance = 0

############### MQTT section ##################
Broker = "192.168.1.10"

snd_topic = "home/receiver" #sub to messages on this topic
rcv_topic = "home/alarmer" #publish messages to this topic

#when receving a message:
def on_message(mqttc, obj, msg):
    global alarmState, distance

    print("subscribing.")
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    try:
        p = msg.payload.decode("utf-8")
        print("decoded payload: " + p)
        valueList = p.split()

        alarmState = valueList[0]
        distance = valueList[1]

        if valueList[2]: #True
            firstTrigger()

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

def snd_msg(buttonHeld, toggle):
    #if data is being sent, that means alarmstate is on!!!
    #dataToSend=json.dumps({"state":[alarmState], , "dist":[distance]})
    valueList = [buttonHeld, toggle]
    stringVal = ' '.join(valueList)
    print("data: " + stringVal)
    mqttc.publish(snd_topic, stringVal)

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
    appendFile("timeFile.txt", "{}\n".format(strftime("%a, %d %b %Y %H:%M:%S"))) #output time to file
    slack.send_msg('#general','Alarm was triggered.') #send slack msg

def timer():
    #send this through mqtt
    snd_msg(True, False)

def toggler():
    #send changed alarm state through mqtt
    snd_msg(False, True)

def showDistance():
    print("distance: " + str(distance))

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

def main():
    alarm()

###################interrupts#######################
holdBtn.when_held = timer
toggleBtn.when_pressed = toggler
distanceBtn.when_pressed = showDistance

#################toplevel script####################
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Closing.")
            #CLEANUP IS AUTOMATIC WITH GPIOZERO
