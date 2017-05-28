import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

###############  global  #####################
valueList = None

############### MQTT section ##################

Broker = "192.168.1.10"

snd_topic = "home/alarmer" #publish messages to this topic
rcv_topic = "home/receiver" #sub to messages on this topic

#when connecting:
def on_connect(mqttc, obj, flags, rc):
    mqttc.subscribe(rcv_topic) #sub

#when receving a message:
def on_message(mqttc, obj, msg):
    global valueList

    print("subscribing.")
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    try:
        p = msg.payload.decode("utf-8")
        print("decoded payload: " + p)
        valueList = p.split()
        return
    except Exception as e:
        print(e)

#when publishing:
def on_publish(mqttc, obj, mid):
    print("publishing.")

#when subscribing:
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

############### assign functions to mqtt ###############
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect(Broker, 1883, 60)
mqttc.loop_start() #or client.loop_forever()

############### more functions ##################
def returnValues():
    if(valueList is not None):
        return valueList #will make the received values available from the outside
    else:
        return "error"

def snd_msg(alarmState, distance):
    #if data is being sent, that means alarmstate is on!!!
    #dataToSend=json.dumps({"state":[alarmState], , "dist":[distance]})
    valueList = [alarmState, distance]
    stringVal = ' '.join(valueList)
    print("data: " + stringVal)
    mqttc.publish(snd_topic, stringVal)

def snd_state(alarmState):
    valueList = [alarmState, distance]
    stringVal = ' '.join(valueList)
    print("data: " + stringVal)
    mqttc.publish(snd_topic, alarmState)
