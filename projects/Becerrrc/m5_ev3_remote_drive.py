#!/usr/bin/env python3
"""
For the full problem statement and details see the corresponding m5_pc_remote_drive.py comments.

There are many solutions to this problem.  The easiest solution on the EV3 side is to NOT bother makes a wrapper
class for the robot object.  Since the challenge presented is very direct it's easiest to just use the Snatch3r class
directly as the delegate to the MQTT client.

The code below is all correct.  The loop_forever line will cause a crash right now.  You need to implement that function
in the Snatch3r class in the library (remember the advice from the lecture).  Pick one team member to implement it then
have everyone else Git update.  Here is some advice for the Snatch3r method loop_forever and it's partner, shutdown.

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.running = False

Additionally you will discover a need to create methods in your Snatch3r class to support drive, shutdown, stop, and
more. Once the EV3 code is ready, run it on the EV3 you can work on the PC side code for the MQTT Remote Control.

Author: David Fisher.
"""
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    retriever = Retriever()
    client = com.MqttClient(retriever)
    client.connect_to_pc()
    retriever.loop_forever()
    # robot = robo.Snatch3r()
    # mqtt_client = com.MqttClient(robot)
    # mqtt_client.connect_to_pc()
    # # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    # robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.

    # color_sensor = ev3.ColorSensor()
    # # Potential values of the color_sensor.color property
    # #   ev3.ColorSensor.COLOR_NOCOLOR is the value 0
    # #   ev3.ColorSensor.COLOR_BLACK   is the value 1
    # #   ev3.ColorSensor.COLOR_BLUE    is the value 2
    # #   ev3.ColorSensor.COLOR_GREEN   is the value 3
    # #   ev3.ColorSensor.COLOR_YELLOW  is the value 4
    # #   ev3.ColorSensor.COLOR_RED     is the value 5
    # #   ev3.ColorSensor.COLOR_WHITE   is the value 6
    # #   ev3.ColorSensor.COLOR_BROWN   is the value 7
    # for k in range(100):
    #     print(color_sensor.reflected_light_intensity, color_sensor.color)
    #     time.sleep(0.5)
    # touch = ev3.TouchSensor()
class Retriever(object):
    def loop_forever(self):
        while True:
            time.sleep(0.05)

    def __init__(self):
        self.color_sensor = ev3.ColorSensor()
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)


        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected

    def color_scan(self):
        self.right_motor.run_forever(speed_sp = 400)
        self.left_motor.run_forever(speed_sp = 400)
        k = 208 / 45

        while True:
            if self.color_sensor.color == 5:
                self.right_motor.run_to_rel_pos(position_sp = -90*k, speed_sp = -400)
                self.left_motor.run_to_rel_pos(position_sp = 90*k, speed_sp = 400)
                self.left_motor.wait_while("running")
                self.right_motor.wait_while("running")
                # self.right_motor.stop()
                # self.left_motor.stop()
                break
            # self.right_motor.run_forever(speed_sp = 400)
            # self.left_motor.run_forever(speed_sp = 400)


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
