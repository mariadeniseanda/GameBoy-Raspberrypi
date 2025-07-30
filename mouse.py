import uinput 
import time
import spidev
import time
import RPi.GPIO as GPIO

pin = 21 #pin connected to button

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)

#open spi
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000
	
events = (
uinput.REL_X,
uinput.REL_Y,
uinput.BTN_LEFT,)

#read channel
def read_channel(ch):
	adc = spi.xfer2([1,(8+ ch)<<4,0])
	val = ((adc[1]&3)<< 8)+ adc[2]
	
	return val

#converting joystick output mouse movment
#515 is the average output for the joycon while idle
def covert_xmove(val):
	if val < 515: #right
		return int((1 - (val/514))*(10))
	else: # val > 515 --> left
		return int((val-514)/514*(-10))

def covert_ymove(val):
	if val < 515:#down
		return int((1 - (val/514))*(-10))
	else: # val > 515 #---> up
		return int((val-514)/514*10)

with uinput.Device(events,name="joystick") as device: #creates a device
	
	try:
		while True:
			x = read_channel(0)
			y = read_channel(1)
			
			print(x,y)
			
			if x in range (518-5,518+5) and y in range (513-5,513+5) : 
				pass
			else:
				device.emit(uinput.REL_X,covert_xmove(x))
				device.emit(uinput.REL_Y,covert_ymove(y))
				
			device.emit(uinput.BTN_LEFT,GPIO.input(pin))
				
			time.sleep(0.2)
	except KeyboardInterrupt:
			print('joystick disconnect')
	finally:
			GPIO.cleanup()
		


		

