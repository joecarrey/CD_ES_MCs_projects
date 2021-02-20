import RPi.GPIO as gpio
import time
import sys
import random

#gpio.setwarnings(False)

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
        
        print(dis)
#         if dis < 30:
#                 
#             #stop()
#             #time.sleep(.05)
#             
#             side = random.choice([True, False])
#             print('Right' if side else 'Left') 
#             count = 0
#             
#             while distance() < 30:
#                 print('Object still there')
#                 turn(side)
#                 time.sleep(.05)
#                 count += 1
#             
#             print('Obgoning')
#             obgon(side, count)
#         elif dis > 1:
#             forward()
#         time.sleep(.05)
        
#         r = gpio.input(26)
#         l = gpio.input(24)
#         
#         if r == 0:
#             left(0.2, 70, 70)
#             print('LEFT')    
#         elif l == 0:
#             right(0.2, 70, 70)
#             print('RIGHT')
#         elif r == 0 and l == 0:
#             break
#         else:
#             forward(0.025, 40, 40)
#         #time.sleep(0.05)    
except KeyboardInterrupt as e:
    print(e)

stop()
gpio.cleanup()
print('Cleaned')


