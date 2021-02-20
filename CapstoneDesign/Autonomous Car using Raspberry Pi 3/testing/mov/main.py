import RPi.GPIO as gpio
import time
import sys
import tkinter as tk
from tkinter import font
import threading

#gpio.setwarnings(False)

SETUP = False
wait_time = 0.06

def distance(measure='cm'):
    #time.sleep(0.3)
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


#def sensor_func():
#    global SETUP
#    print('Thread started')
#    print(SETUP)
#    if SETUP:
#        while True:
#            while not gpio.input(12):
#                print('Forward')

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
    global wait_time
    
    gpio.output(12, True)
    gpio.output(16, False)
    gpio.output(18, False)
    gpio.output(22, True)
    time.sleep(wait_time)
    
def left():
    global wait_time
    
    gpio.output(12, False)
    gpio.output(16, True)
    gpio.output(18, True)
    gpio.output(22, False)
    time.sleep(wait_time)

def key_input(event):
    print("Key:", event.char)
    key_press = event.char
    
    curDis = distance("cm")
    print("Distance:", curDis)
    
    if curDis > 15:
        if key_press.lower() == "w":
            forward()
        elif key_press.lower() == "s":
            reverse()
        elif key_press.lower() == "a":
            left()
        elif key_press.lower() == "d":
            right()
        elif key_press.lower() == " ":
            stop() 
        else:
            pass

init()

#x = threading.Thread(target=sensor_func)
#x.start()

master = tk.Tk()
master.grid()

f = font.Font(family='Calibri', size=12)

master.geometry('410x345')

master.bind('<KeyPress>', key_input)

button1 = tk.Button(master, text="W", command=forward, width='10', height='5', font=f)
button1.grid(row=0, column=1)

button2 = tk.Button(master, text="A", command=left, width='10', height='5', font=f)
button2.grid(row=1, column=0)

button3 = tk.Button(master, text="SPACE", command=stop, width='10', height='5', font=f)
button3.grid(row=1, column=1, padx=10, pady=10)

button4 = tk.Button(master, text="D", command=right, width='10', height='5', font=f)
button4.grid(row=1, column=2)

button5 = tk.Button(master, text="S", command=reverse, width='10', height='5', font=f)
button5.grid(row=2, column=1)

master.mainloop()

gpio.cleanup()
SETUP = False
#x.join()
print('Cleaned')