import RPi.GPIO as gpio
import time
import sys
import random

p1 = None
p2 = None
p3 = None
p4 = None

MAX_SPEED = 100

def distance():
    gpio.output(38, True)
    time.sleep(0.00001)
    
    sig, nosig = 0, 0
    gpio.output(38, False)
    while gpio.input(40) == 0:
        nosig = time.time()
    
    while gpio.input(40) == 1:
        sig = time.time()
    
    tl = sig - nosig
    
    #if tl == 0:
        #return distance()
    
    return tl / 0.000058

def init():
    
    try:
        gpio.setmode(gpio.BOARD)
        gpio.setup(12, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        gpio.setup(22, gpio.OUT)
        gpio.setup(38, gpio.OUT)
        gpio.setup(40, gpio.IN)
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
try:
    while True:
        #print(distance())
        x = distance()
        if x < 3 or x > 2200:
            continue    
            
        print(x)
        if x > 27 and x < 33:
            stop()
        elif x > 33:
            forward(.05)
        else:
            reverse(.05)
            stop()
        time.sleep(.01)
except Exception as e:
    print(e)
    pass

# END TASK 1

# TASK 2

#try:
#    while True:
#        if distance() < 30:
#            reverse(.5)
#            if random.choice([True, False]):
#                right(.3)
#            else:
#                left(.3)
#            if distance() < 30:
#                continue
#            forward(2)
#            stop()
#            break
#        else:
#            forward(.05)
#except Exception as e:
#    print(e)
#    pass

# END TASK 2

# TASK 3

#try:
#    while True:
#        x = distance()
#        if x < 25:
#            stop()
#        elif x < 100:
#            forward(.05, 80, 80)
#        else:
#            forward(.05)
#except Exception as e:
#    pass

# END TASK 3

gpio.cleanup()
