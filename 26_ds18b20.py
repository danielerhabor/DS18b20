
import os
import RPi.GPIO as gpio
pin1 = 27
pin2 = 18
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(pin1,gpio.OUT)
gpio.setup(pin2,gpio.OUT)

ds18b20 = '28-0115a2b0beff'         # Sensor ID
def setup():
    global ds18b20
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1-bus-master1':
            ds18b20 = i
def read():

    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    return temperature

def loop():
    while True:
        temp = read()
        if  temp != None:
            if temp <= 24:                          #If the tempereature was less than or equal to 24 degrees
                gpio.output(pin1, True)             # turn on the BLUE LED else turn it off
            else:
                gpio.output(pin1, False)            # If the temperature was greater than or equal to 24 degrees
            if temp >= 27:                          # turn on the RED LED else turn it off
                gpio.output(pin2, True)
            else:
                gpio.output(pin2, False)
            print "Current temperature : %0.3f C" % temp
def destroy():
    pass
if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
 
