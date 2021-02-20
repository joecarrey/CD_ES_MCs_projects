import RPi.GPIO as gpio
import time
import sys
import random

#gpio.setwarnings(False)


def distance():
    gpio.output(38, True)
    time.sleep(0.00001)
    
    gpio.output(38, False)
    while gpio.input(40) == 0:
        nosig = time.time()
    
    while gpio.input(40) == 1:
        sig = time.time()
    
    tl = sig - nosig
    print(tl / 0.000058)    
    return tl / 0.000058


def init():
    
    try:
        gpio.setmode(gpio.BOARD)
        gpio.setup(12, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        gpio.setup(22, gpio.OUT)
        gpio.setup(24, gpio.IN)
        gpio.setup(26, gpio.IN)
        
        gpio.setup(32, gpio.IN)
        gpio.setup(36, gpio.IN)
        
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
    
def ir_sensor():
    if r == 0:
        left(.1, 65, 65)
        print('LEFT')    
    elif l == 0:
        right(.1, 65, 65)
        print('RIGHT')
    #elif r == 0 and l == 0:
        #break
    #else:
#         forward(0.025, 55, 55)
        #break
    
def obgon():    
    side = random.choice([True, False])
        
    if side:
        right(.5, 40, 40)
    else:
        left(.5, 40, 40)
    
    forward(.8, 55, 55)
    if not side:
        right(.5, 50, 50)
        forward(.8, 55, 55)
        right(.5, 50, 50)
        forward(1.1, 55, 55)
        left(.5, 50, 50)
    else:
        left(.5, 50, 50)
        forward(.8, 55, 55)
        left(.5, 50, 50)
        forward(1.1, 55, 55)
        right(.5, 50, 50)
    
    forward(1.3, 55, 55)

    reverse(0.3, 50, 50)
    right(1.02, 50, 50)
    reverse(1.8, 50, 50)
            
init()

p1 = gpio.PWM(12, 100)
p2 = gpio.PWM(16, 100)
p3 = gpio.PWM(18, 100)
p4 = gpio.PWM(22, 100)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

flag = True

try:
    while True:
        r = gpio.input(26)
        l = gpio.input(24)
         
        ir_sensor()

        dist = distance()
        
        if flag and dist < 30:
            while distance() < 30:
                stop()
                time.sleep(.5)
            flag = False
            continue

        if not flag and dist < 30:
            obgon()
            break
            
        
        forward(0.015, 40, 40)
        
        #time.sleep(0.05)    
except KeyboardInterrupt as e:
    print(e)

stop()
gpio.cleanup()
print('Cleaned')

