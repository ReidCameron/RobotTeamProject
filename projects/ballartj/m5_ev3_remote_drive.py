import robot_controller as robo
import time
import mqtt_remote_method_calls as com


class Beacon(object):

    def __init__(self):
        self.robot = robo.Snatch3r()

    def loop_forver(self):
        while True:
            time.sleep(.05)

    def arm_up(self):
        self.robot.arm_up()

    def arm_down(self):
        self.robot.arm_down()

    def send_forward(self):
        self.robot.forward(self)

    def finder(self):
        self.send_left()
        if self.robot.beacon_finder.distance <=10:
            self.robot.stop()
            time.sleep(.5)
            self.send_forward()




def main():
    remote = Beacon()
    mqtt_client = com.MqttClient(remote)
    mqtt_client.connect_to_pc()
    remote.loop_forever()

main()
