"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.close = False

        assert self.touch_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected

        print("Arm is Calibrating.")
        self.arm_calibration()
        print("Done:)")

    def forward(self, inches, speed, stop_action = 'brake'):
        k = 360 / 4.2
        degrees = (k*inches)
        self.left_motor.run_to_rel_pos(speed_sp = speed * 8,
                                       position_sp = degrees,
                                       stop_action = stop_action)
        self.right_motor.run_to_rel_pos(speed_sp=speed * 8,
                                       position_sp=degrees,
                                       stop_action=stop_action)
        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")
    def backward_inches(self, inches, speed, stop_action = 'brake'):
        k = 360 / 4.2
        degrees = (k*inches)
        self.left_motor.run_to_rel_pos(speed_sp = speed * -8,
                                       position_sp = -1*degrees,
                                       stop_action = stop_action)
        self.right_motor.run_to_rel_pos(speed_sp=speed * -8,
                                       position_sp=-1*degrees,
                                       stop_action=stop_action)
        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")
    def move(self,speed_right,speed_left):
        self.left_motor.run_forever(speed_sp = speed_left)
        self.right_motor.run_forever(speed_sp= speed_right)

    def spin_left_by_time(self,degrees, speed, brake_action = 'brake'):
        # degrees = inches * (360 / 13)  # 5 inches for 1 wheel rotation
        k=0.8
        time_needed = (degrees / speed) * k
        print(time_needed)
        self.left_motor.run_forever(speed_sp=-speed * 8)
        self. right_motor.run_forever(speed_sp=speed * 8)
        time.sleep(time_needed)
        self.left_motor.stop(stop_action=brake_action)
        self.right_motor.stop(stop_action=brake_action)
    def spin_by_encoders(self,degrees, speed, brake_action = 'brake'):

        k=208/45
        degrees_needed = degrees*k
        print(degrees_needed)

        self.left_motor.run_to_rel_pos(speed_sp=-speed * 8,
                                       position_sp = degrees_needed)
        self.right_motor.run_to_rel_pos(speed_sp=speed * 8,
                                       position_sp=degrees_needed)
        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")
    def spin(self,right_speed, left_speed):
        self.right_motor.run_forever(speed_sp = right_speed)
        self.left_motor.run_forever(speed_sp = left_speed)
    def loop_forever(self):
        while True:
            if self.close == True:
                break
            time.sleep(0.05)
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=700)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def arm_down(self):
        self.arm_motor.run_to_rel_pos(position_sp=-14.2*360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=700)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="coast")
        print("Benchmark 1")
        arm_revolutions_for_full_range = 14.2*360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while('running')
        print("Benchmark 2")
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).
    def shutdown(self):
        self.close = True