# Import the Python libraries needed
import RPi.GPIO as gpio
import time
import random
import math


def bound_duty_cycle(val):
    return round(max(0.0, min(100.0, val)))


print("Starting...")

# Set the LED GPIO number
ledGpio = 21

# Set the GPIO mode to Broadcom pin numbers, not Board pin numbers
gpio.setmode(gpio.BCM)

# Set the LED GPIO pin as an output
gpio.setup(ledGpio, gpio.OUT)

# Setup pulse-width modulation
refreshHtz = 300
startingPower = 0
pwm = gpio.PWM(ledGpio, refreshHtz)
pwm.start(startingPower)

averageLevel = 60.0
levelVariance = 15.0
varianceHtz = 0.25

flickerMaxLevel = 30.0
flickerHtz = 5.0
flickerDampening = 0.4
flickerDuration = 4.0
flickerDelay = 8.0

timeAccum = 0.0
flickerTimeAccum = 0.0
timeStep = 0.01
isFlicker = False

try:
    while True:
        level = averageLevel - levelVariance * math.cos((2.0 * varianceHtz) * math.pi * timeAccum)

        if flickerDelay <= 0.0:
            flickerTimeAccum = 0.0
            flickerMaxLevel = random.uniform(20.0, 40.0)
#            flickerHtz = random.uniform(4.0, 6.0)
            flickerDampening = random.uniform(0.2, 0.6)
            flickerDuration = float(random.randint(3, 6))
            flickerDelay = random.uniform(1.0, 10.0)
            isFlicker = True

        if isFlicker:
            flickerLevel = flickerMaxLevel / 2.0 * math.pow(math.e, -flickerDampening * flickerTimeAccum)
#            adjustedFlickerLevel = flickerLevel - flickerLevel * math.cos(2.0 * flickerHtz * math.pi * flickerTimeAccum)
            adjustedFlickerLevel = flickerLevel * (1 - math.cos(2.0 * flickerHtz * math.pi * flickerTimeAccum))
            flickerTimeAccum += timeStep
            level += adjustedFlickerLevel
            if flickerTimeAccum >= flickerDuration:
                isFlicker = False

        pwm.ChangeDutyCycle(bound_duty_cycle(level))

        flickerDelay -= timeStep
        timeAccum += timeStep
        time.sleep(timeStep)

except KeyboardInterrupt:
    pass

# Clean up
pwm.stop()
gpio.cleanup()

print("Complete")
