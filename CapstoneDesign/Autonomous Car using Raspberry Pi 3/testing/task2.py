import RPi.GPIO as gpio
import time
import sys

wait_time = 0.06
p1 = None
p2 = None
p3 = None
p4 = None

def init():
    global SETUP
    
    try:
        gpio.setmode(gpio.BOARD)
        gpio.setup(12, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        gpio.setup(22, gpio.OUT)
    except Exception as e:
        gpio.cleanup()
        init()
    SETUP = True

def stop():
    global wait_time
    
    gpio.output(12, False)
    gpio.output(16, False)
    gpio.output(18, False)
    gpio.output(22, False)
    time.sleep(wait_time)

def reverse():
    global wait_time
    
    gpio.output(12, False)
    gpio.output(16, True)
    gpio.output(18, False)
    gpio.output(22, True)
    time.sleep(wait_time)
    
def forward():
    global wait_time
    
    gpio.output(12, True)
    gpio.output(16, False)
    gpio.output(18, True)
    gpio.output(22, False)
    time.sleep(wait_time)

def right():
	
    gpio.output(12, True)
    gpio.output(16, False)
    gpio.output(18, False)
    gpio.output(22, True)
    time.sleep(1.75)
    
def left():
	
    gpio.output(12, False)
    gpio.output(16, True)
    gpio.output(18, True)
    gpio.output(22, False)
    time.sleep(1.75)


def smooth_right():
	
	p1.ChangeDutyCycle(100)
	p2.ChangeDutyCycle(0)
	p3.ChangeDutyCycle(10)
	p4.ChangeDutyCycle(0)
	
	time.sleep(5)

def smooth_left():
	
	p1.ChangeDutyCycle(0)
	p2.ChangeDutyCycle(10)
	p3.ChangeDutyCycle(100)
	p4.ChangeDutyCycle(0)
	
	time.sleep(5)

init()
#right()
#time.sleep(.5)
#left()

p1 = gpio.PWM(12, 100)
p2 = gpio.PWM(16, 100)
p3 = gpio.PWM(18, 100)
p4 = gpio.PWM(22, 100)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

#smooth_right()
#smooth_left()
forward()
#reverse()
#stop()

gpio.cleanup()
