#Axelle Jamous s090603 2EA1

from gpiozero import LED, Button
import time

#setup
led1 = LED(4)
led2 = LED(17)
led3 = LED(27)
led4 = LED(22)
led5 = LED(18)
button = Button(14)

arrLeds = [led1,led2,led3,led4,led5]
prevLed = prevLed2 = 0
delay = 2
arrIndex = -1 #because otherwise it'll skip the first one

#functions
def pressed(btn):
	global delay	
	global prevLed2

	if led3.is_lit:
		if delay > 0.5:
			#hit
			delay -= 0.3 #speed up
			print("Hit!")
		else:
			delay = 2
	else:
		#definite miss cause led isn't on
		delay = 2
		print("Sorry you missed it!")
	
	prevLed2 = timer
	

#main
while True:
	timer = time.time()
	arrLeds[arrIndex].on()

	if timer-prevLed >= delay:
		if arrIndex > 3:
			arrIndex = -1

		arrLeds[arrIndex].off()
		arrIndex+=1
		prevLed = timer

	if timer-prevLed2 >= delay:
		button.when_pressed = pressed #call pressed fct when pressed
