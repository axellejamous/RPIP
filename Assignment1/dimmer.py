from gpiozero import PWMLED, Button

#setup
led = PWMLED(17)
button = Button(14)
brightness = 0 #off

#functions
def pressed(btn):
	global brightness

	print("button clicked " + str(brightness))

	if brightness >= 1: 	
		brightness = 0 #reset 

	elif brightness >= 0 and brightness < 1:
		brightness+=0.1

	else:
		#err
		print("error: " + brightness)

	led.value = brightness

#main
while True:
	print("before press " + str(brightness))
        button.when_pressed = pressed #call pressed fct when pressed
