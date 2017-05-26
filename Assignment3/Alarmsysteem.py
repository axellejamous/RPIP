import RPi.GPIO as GPIO
import time
if __name__ == "__main__":
	try:
		pinButton=5
		pinSensor=11
		pinLed=3
		btnDown=False
		btnUpTime=None
		alarmOn=False
		ledState=False
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pinButton,GPIO.IN)
		GPIO.setup(pinSensor,GPIO.IN)
		GPIO.setup(pinLed, GPIO.OUT)
		def button_interaction(self):
			global btnUpTime
			global btnDown
			global alarmOn
			if(GPIO.input(pinButton)):
				print("Rising edge detected")
				btnUpTime=millis()
				btnDown=True
			else:
				print("Falling edge detected")
				if(btnDown):
					if(millis()>=btnUpTime+5000):
						alarmOn=False
				btnDown=False
		def sensed(self):
			global alarmOn
			alarmOn=True
			file=open("alarmlogs","a")
			file.write(time.strftime("%a, %d %b %Y %H:%M:%S")+"\n")
			file.close()
		def millis():
			return int(round(time.time()*1000))
		GPIO.add_event_detect(pinButton,GPIO.BOTH,button_interaction)
		GPIO.add_event_detect(pinSensor,GPIO.RISING,sensed, bouncetime=300)
		while(True):
			if(alarmOn):
				ledState = not ledState
			else:
				ledState=False
			GPIO.output(pinLed,ledState)
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("Closing.")
		GPIO.cleanup()
