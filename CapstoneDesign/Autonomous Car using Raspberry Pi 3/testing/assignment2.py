import RPi.GPIO as gpio
import time
import sys

p1 = None
p2 = None
p3 = None
p4 = None

MAX_SPEED = 100

def init():
    
    try:
        gpio.setmode(gpio.BOARD)
        gpio.setup(12, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        gpio.setup(22, gpio.OUT)
    except Exception as e:
        gpio.cleanup()
        init()

def stop():
    
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)

def reverse(wt, x=100, y=100):
    
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(x)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(y)
    time.sleep(wt)
    
def forward(wt, x=100, y=100):
    
    p1.ChangeDutyCycle(x)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(y)
    p4.ChangeDutyCycle(0)
    time.sleep(wt)

def right(wt, x=100, y=100):
	
    p1.ChangeDutyCycle(x)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(y)
    time.sleep(wt)
    
def left(wt, x=100, y=100):
	
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(x)
    p3.ChangeDutyCycle(y)
    p4.ChangeDutyCycle(0)
    time.sleep(wt)

init()

p1 = gpio.PWM(12, MAX_SPEED)
p2 = gpio.PWM(16, MAX_SPEED)
p3 = gpio.PWM(18, MAX_SPEED)
p4 = gpio.PWM(22, MAX_SPEED)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)


# TASK 1

#forward(2)

#stop()
#time.sleep(1)

#right(.335)

#stop()

#reverse(2)

#stop()
#time.sleep(1)

#left(.335)
#stop()

# END TASK 1

# TASK 2

#right(1.4)

#stop()
#time.sleep(1)

#left(1.4)

# END TASK 2

# TASK 3

#for i in range(1, 10):
#    forward(.05, i * 10, i * 10)
#    time.sleep(1)
#stop()

# END TASK 3

# TASK 4

#forward(1, 100, 30)
#stop()
#forward(1, 30, 100)
#stop()

# END TASK 4

gpio.cleanup()
