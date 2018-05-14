import ev3dev.ev3 as ev3
import math
import time

import robot_controller as robo

my_robot = robo.Snatch3r()
def main():
    while True:
        speed = int(input('Enter a speed: '))
        if speed <= 0:
            break
        degrees = int(input('Enter a turn: '))
        if degrees <= 0:
            break
        my_robot.spin_left(degrees,speed)
main()
print("Session is done:)")