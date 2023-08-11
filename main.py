import os
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print('Press the button')
while True:
    button_state = GPIO.input(26)

    if button_state == False:
        print('Exceute the task')
        python /Users/athre/Desktop/Raspberry-Face-Recognition-master
        time.sleep(1)
