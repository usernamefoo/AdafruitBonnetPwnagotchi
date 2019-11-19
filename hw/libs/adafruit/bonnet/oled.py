# Driver for Adafruit 128x62 1.3" OLED bonnet (based on oledhat)
# 
# Must install Adafruit_CircuitPython_SSD1306
# 'sudo pip3 install adafruit-circuitpython-ssd1306'
#
# Keys are set up as
# 5 - Sleep or wake up screen
# 6 - Short press AUTO, long press(3s) shutdown
# L - Turn off Screen Saver
# R - Trun On Screen Saver
# U - Flip screen up
# D - Flip screen down

import time
import subprocess
import logging

import RPi.GPIO as GPIO

import busio
import adafruit_ssd1306

#Screen saver timeout
TIMEOUT = 300

# Display resolution
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Pin definitions
SCL = 3
SDA = 2

BUTTON_A = 5
BUTTON_B = 6
BUTTON_L = 27
BUTTON_R = 23
BUTTON_U = 17
BUTTON_D = 22
BUTTON_C = 4

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH ,OLED_HEIGHT, i2c)

class Display(object):

    def __init__(self):
        self.TIMEOUT = TIMEOUT
        self.DISPLAY_TIME = time.time()
        self.ROTATE = 180
        self.SHUTDOWN = 'shutdown -h now'
        self.AUTO = 'touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi'
        self.SLEEP = True
        
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(BUTTON_A, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(BUTTON_B, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(BUTTON_U, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(BUTTON_D, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(BUTTON_C, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(BUTTON_L, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(BUTTON_R, GPIO.IN, GPIO.PUD_UP)

        GPIO.add_event_detect(BUTTON_A, GPIO.FALLING, callback=self.screen_power, bouncetime=300)
        GPIO.add_event_detect(BUTTON_B, GPIO.FALLING, callback=self.util_button, bouncetime=300)

        GPIO.add_event_detect(BUTTON_U, GPIO.FALLING, callback=self.rotate, bouncetime=300)
        GPIO.add_event_detect(BUTTON_D, GPIO.FALLING, callback=self.rotate, bouncetime=300)
        
        GPIO.add_event_detect(BUTTON_L, GPIO.FALLING, callback=self.sleep, bouncetime=300)
        GPIO.add_event_detect(BUTTON_R, GPIO.FALLING, callback=self.sleep, bouncetime=300)

    def rotate(self, pin):
        if pin == BUTTON_U:
            self.ROTATE = 180
        if pin == BUTTON_D:
            self.ROTATE = 0

    def sleep(self, pin):
        if pin == BUTTON_L:
            self.SLEEP = False
        if pin == BUTTON_R:
            self.SLEEP = True
            self.DISPLAY_TIME = time.time()
        
    def screen_power(self, pin):
        if not disp.power:
            disp.poweron()
            self.DISPLAY_TIME = time.time()
        else:
            disp.poweroff()

    def util_button(self, pin):
        start_time = time.time()
        
        while GPIO.input(pin) == 0: # Wait for the button up
            pass
            
        buttonTime = time.time() - start_time
        
        # Check for Auto short press
        if .5 <= buttonTime <= 3:    
            subprocess.Popen(self.AUTO, shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None,
                            executable="/bin/bash")
        # Check for shutdown long press      
        elif buttonTime > 3:         
           subprocess.Popen(self.SHUTDOWN, shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None,
                            executable="/bin/bash")
           disp.poweroff() 
                            
    def init(self):
        disp.invert(True)
        disp.fill(0)
        disp.show()

    def display(self, image):
        # Check display time out
        now = time.time()
        if  (now - self.DISPLAY_TIME > self.TIMEOUT) and self.SLEEP:
            disp.poweroff()
                            
        disp.image(image.rotate(self.ROTATE))
        disp.show()

    def clear(self):
        disp.fill(0)
        disp.show()
        
