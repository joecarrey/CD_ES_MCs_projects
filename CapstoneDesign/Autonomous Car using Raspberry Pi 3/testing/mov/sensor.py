import RPi.GPIO as gpio
import time

def distance(measure='cm'):
    time.sleep(0.3)
    gpio.output(38, True)
    time.sleep(0.00001)
    
    gpio.output(38, False)
    while gpio.input(40) == 0:
        nosig = time.time()
    
    while gpio.input(40) == 1:
        sig = time.time()
    
    tl = sig - nosig
    
    if measure == 'cm':
        distance = tl / 0.000058
    elif measure == 'in':
        distance = tl / 0.000148
    else:
        print('Improper choice of measurement: in or cm')
        distance = None
    
    return distance
  
print(distance('cm'))
    