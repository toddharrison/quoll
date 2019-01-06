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

a = 60.0
b = 10.0
c = 4.0

d = 30.0
f = 5.0
g = 0.6
h = 0.0
i = 8.0

x = 0.0
x2 = 0.0
step = 0.01
flicker = False

try:
    while True:
        y = a - b * math.cos((2.0 / c) * math.pi * x)

        if i <= 0.0:
            x2 = 0.0
            d = random.uniform(20.0, 40.0)
#            f = random.uniform(4.0, 6.0)
            g = random.uniform(0.4, 0.8)
            h = random.uniform(3.0, 5.0)
            i = 8.0
            flicker = True

        if flicker:
            pre = d / 2.0 * math.pow(math.e, -g * x2)
            y2 = pre - pre * math.cos(2.0 * f * math.pi * x2)
            x2 += step
            y += y2
            if x2 >= h:
                flicker = False

        pwm.ChangeDutyCycle(round(max(0.0, min(100.0, y))))

        i -= step
        x += step
        time.sleep(step)

except KeyboardInterrupt:
    pass

# Clean up
pwm.stop()
GPIO.cleanup()

print("Complete")
