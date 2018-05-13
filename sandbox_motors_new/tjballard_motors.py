"""
Functions for SPINNING the robot LEFT and RIGHT.
Authors: David Fisher, David Mutchler and TJ Ballard.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# DONE: 2. Implment spin_left_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for spin_left_by_time.
#   Then repeat for spin_left_by_encoders.
#   Then repeat for the spin_right functions.


import ev3dev.ev3 as ev3
import time


def test_spin_left_spin_right():
    """
    Tests the spin_left and spin_right functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets degrees and runs spin_left_by_time.
      3. Same as #2, but runs spin_left_by_encoders.
      4. Same as #1, 2, 3, but tests the spin_right functions.
    """
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    assert left_motor.connected
    assert right_motor.connected

    seconds = 1
    while seconds != 0:
        inches = float(input('Distance(inches): '))
        seconds = int(input("Enter a time for the robot to travel: "))
        speed = int(input("Enter a speed for the motors (0 to 900 dps): "))
        stop_action = input("Enter a break action: ")
        degrees = int(input("Enter Degrees: "))
        spin_left_seconds(seconds, speed, stop_action)
        spin_left_by_time(degrees, speed, stop_action)
        spin_left_by_encoders(degrees, speed, stop_action)
        spin_right_seconds(seconds, speed, stop_action)
        spin_right_by_time(degrees, speed, stop_action)
        spin_right_by_encoders(degrees, speed, stop_action)




def spin_left_seconds(seconds, speed, stop_action):
    """
    Makes the robot spin in place left for the given number of seconds at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the given stop_action.
    """

    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    assert left_motor.connected
    assert right_motor.connected

    left_motor.run_forever(speed_sp=-speed * 8)
    right_motor.run_forever(speed_sp=speed * 8)
    time.sleep(seconds)
    left_motor.stop(stop_action="brake")
    right_motor.stop(stop_action="brake")


def spin_left_by_time(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    assert left_motor.connected
    assert right_motor.connected

    time_needed = float(inches / (speed / 10))

    left_motor.run_forever(speed_sp=-speed * 8)
    right_motor.run_forever(speed_sp=speed * 8)
    time.sleep(time_needed)
    left_motor.stop(stop_action="brake")
    right_motor.stop(stop_action="brake")


def spin_left_by_encoders(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should spin to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    assert left_motor.connected
    assert right_motor.connected

    degrees = inches * (360 / 13)  # 5 inches for 1 wheel rotation
    time_needed = degrees * ((inches / (speed / 10)) / 360)

    left_motor.run_forever(speed_sp=-speed * 8)
    right_motor.run_forever(speed_sp=speed * 8)
    time.sleep(time_needed)
    left_motor.stop(stop_action="brake")
    right_motor.stop(stop_action="brake")


def spin_right_seconds(seconds, speed, stop_action):
    """ Calls spin_left_seconds with negative speeds to achieve spin_right motion. """
    speed = -1*speed
    spin_left_seconds(seconds, speed, stop_action)


def spin_right_by_time(degrees, speed, stop_action):
    """ Calls spin_left_by_time with negative speeds to achieve spin_right motion. """
    speed = -1 * speed
    spin_left_by_time(degrees, speed, stop_action)


def spin_right_by_encoders(degrees, speed, stop_action):
    """ Calls spin_left_by_encoders with negative speeds to achieve spin_right motion. """
    speed = -1 * speed
    spin_left_by_encoders(degrees, speed, stop_action)


test_spin_left_spin_right()