#alarmsysteem Axelle Jamous 2EA1

from gpiozero import DistanceSensor


ultrasonic = DistanceSensor(echo=17, trigger=4) #echo and trigger pins
#if u want to change the default threshold distance/max distance (see below) use this code:
#ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)
#ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=2)

#or after the sensor is created:
#ultrasonic.threshold_distance = 0.5
#ultrasonic.max_distance = 2

def hello():
    print("Hello")

def bye():
    print("Bye")

while True:
    print(ultrasonic.distance) #show distance

    #do something when in and out of range
    #The default range threshold is 0.3m and default maximum is 1m
    #wait_for = blocking program is on halt until triggered
    #ultrasonic.wait_for_in_range() = hello
    #ultrasonic.wait_for_out_of_range() = bye

    #when triggers actions in the background while other code is happening:
    ultrasonic.when_in_range() = hello
    ultrasonic.when_out_of_range() = bye

