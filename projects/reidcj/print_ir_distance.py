#!/usr/bin/env python3
"""
The goal of this example is to show you the syntax for IR distance readings.  Additionally
it's good to play with a demo so that you can see how well or not well a sensor behaves.
To test this module run it, place the IR Sensor at 0 cm on your ruler, then hold a white
sheet of paper some distance away.  Watch the values print as you move the paper closer and
farther away.  How well do the values match the number of centimeters away?

Authors: David Fisher.
"""

import ev3dev.ev3 as ev3
import time


def main():
    print("--------------------------------------------")
    print(" Printing distances")
    print("--------------------------------------------")
    ev3.Sound.speak("Printing distance").wait()
    print(" Press the touch sensor to exit")

    touch_sensor = ev3.TouchSensor()
    ir_sensor = ev3.InfraredSensor()
    assert touch_sensor
    assert ir_sensor

    readings = []
    def setup(x):
        for _ in range(5):
            readings.append(x)
    def averager(x):
        average = 0
        for k in range(4):
            readings[k] = readings[k+1]
        readings[4] = x
        for j in range(5):
            average = average + 0.2*readings[j]
        return average
    k = 0
    while not touch_sensor.is_pressed:
        current_proximity = ir_sensor.proximity
        if k == 0:
            setup(current_proximity)
            k = 1
        x = averager(current_proximity)
        print("IR Distance = {}".format(current_proximity), "           ",  int(x))
        time.sleep(0.01)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
