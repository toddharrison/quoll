# Import the Python libraries needed
import RPi.GPIO as GPIO
import time
import random
import math

print("Starting...")

# Set the LED GPIO number
LED_GPIO = 21

# Set the GPIO mode to Broadcom pin numbers, not Board pin numbers
GPIO.setmode(GPIO.BCM)

# Set the LED GPIO pin as an output
GPIO.setup(LED_GPIO, GPIO.OUT)

# Setup pulse-width modulation
refreshHtz = 300
startingPower = 0
pwm = GPIO.PWM(LED_GPIO, refreshHtz)
pwm.start(startingPower)

try:
    while True:
        for dc in range(0, 101, 2):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.02)
        for dc in range(100, -1, -2):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.02)

except KeyboardInterrupt:
    pass

# Clean up
pwm.stop()
GPIO.cleanup()

print("Complete")
