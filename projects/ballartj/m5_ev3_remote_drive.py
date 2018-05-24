import robot_controller as robo
import time
import mqtt_remote_method_calls as com


class Beacon(object):

    def __init__(self):
        self.robot = robo.Snatch3r()

    def loop_forever(self):
        while True:
            time.sleep(.05)

    def stop(self):
        self.robot.stop()

    def send_forward(self):
        self.robot.move(600, 600)

    def send_right(self):
        self.robot.spin(-200, 200)

    def send_left(self):
        self.robot.spin(250, -250)

    def finder(self):
        while self.robot.ir_sensor.proximity > 95:
            print('nothing is being detected', self.robot.ir_sensor.proximity)
            self.send_right()
        while self.robot.ir_sensor.proximity > 15:
            print('Detected', self.robot.ir_sensor.proximity)
            print(self.robot.ir_sensor.proximity)
            self.send_forward()
        print(self.robot.ir_sensor.proximity)
        self.stop()
        self.robot.blinking_lights()


def main():
    remote = Beacon()
    mqtt_client = com.MqttClient(remote)
    mqtt_client.connect_to_pc()
    remote.loop_forever()


main()
