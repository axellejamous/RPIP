from gpiozero import LED, Button
from time import sleep
from random import uniform

#setup
led = LED(4)
button = Button(14)
state = 0 #off

#functions
def pressed(btn):
	global state

	print('button pressed')
	if state == 0:
		led.on()
		state = 1
	elif state == 1: 	
		led.off()
		state = 0
	else:
		#err
		state = -1

#main
while True:
        button.when_pressed = pressed #call pressed fct when pressed
