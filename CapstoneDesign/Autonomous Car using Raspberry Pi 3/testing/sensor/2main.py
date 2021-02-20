import RPi.GPIO as gpio
import time
import sys
import random

#gpio.setwarnings(False)

wait_time = 0.06

def distance():
    gpio.output(38, True)
    time.sleep(0.00001)
    gpio.output(38, False)
    
    nosig = 0
    sig = 0
    while gpio.input(40) == 0:
        nosig = time.time()
        
    while gpio.input(40) == 1:
        sig = time.time()

    tl = sig - nosig
    if tl == 0:
        return 1
    return tl / 0.000058

def init():
    global SETUP
    
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
    SETUP = True

def stop():
    global wait_time
    
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    time.sleep(wait_time)

def reverse():
    global wait_time
    
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(50)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(50)
    
    time.sleep(wait_time)
    
def forward():
    global wait_time
    
    p1.ChangeDutyCycle(50)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(50)
    p4.ChangeDutyCycle(0)
    
    time.sleep(wait_time)
    
def right():
    global wait_time
    
    p1.ChangeDutyCycle(80)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(80)
    
    time.sleep(wait_time)
    
def left():
    global wait_time
    
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(80)
    p3.ChangeDutyCycle(80)
    p4.ChangeDutyCycle(0)

    time.sleep(wait_time)
        
        
def turn(side, negate=False):
    side = side != negate
    
    if side:
        right()
    else:
        left()
    time.sleep(.35)
        
def obgon(side, count):
    forward()
    time.sleep(1)

    turn(side, negate=True)
    time.sleep(count * 0.05)
    
    #dis = distance()
    #if dis < 30:
    #    turn(side)
    #    obgon(side, count * 0.05)
    forward()
    time.sleep(1)
    
    turn(side, negate=True)
    time.sleep(count * 0.05)
    
    #dis = distance()
    #if dis < 30:
    #    turn(side)
    #    obgon(side, count * 0.05)
    forward()
    time.sleep(1)
    
    turn(side)
    time.sleep(count * 0.05)
    
    #dis = distance()
    #if dis < 30:
    #    turn(side)
    #    obgon(side, count * 0.05)
    forward()
    time.sleep(1)

init()

p1 = gpio.PWM(12, 100)
p2 = gpio.PWM(16, 100)
p3 = gpio.PWM(18, 100)
p4 = gpio.PWM(22, 100)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

try:
    while True:
        dis = distance()
        print('Object found')
        #print(dis)
        if dis < 30:
                
            #stop()
            #time.sleep(.05)
            
            side = random.choice([True, False])
            print('Right' if side else 'Left') 
            count = 0
            
            while distance() < 30:
                print('Object still there')
                turn(side)
                time.sleep(.05)
                count += 1
            
            print('Obgoning')
            obgon(side, count)
        elif dis > 1:
            forward()
        time.sleep(.05)
except KeyboardInterrupt as e:
    print(e)

stop()
gpio.cleanup()
print('Cleaned')
