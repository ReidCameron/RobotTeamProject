import turtle
import tkinter as tk
import mqtt_remote_method_calls as com
import time


def forward(mqtt_client, t):
    print("forward")
    global is_stopped
    while True:
        if is_stopped == True:
            stop(mqtt_client)
            break
        mqtt_client.send_message("move", [300,300])
        t.forward(1)
        # mqtt_client.send_message("detector")
        time.sleep(0.01)


def back(mqtt_client, t):
    print("back")
    global is_stopped
    while True:
        if is_stopped == True:
            stop(mqtt_client)
            break
        mqtt_client.send_message("move", [-300, -300])
        t.backward(1)
        time.sleep(0.01)
    is_stopped = False


def left(mqtt_client, degrees, t):
    print("left")
    mqtt_client.send_message("spin_left", [degrees])
    t.left(90)


def right(mqtt_client, degrees, t):
    print("right")
    mqtt_client.send_message("spin_right", [degrees])
    t.right(90)


def stop(mqtt_client):
    print("stop")
    global is_stopped
    is_stopped = True
    mqtt_client.send_message("stop")


def return_home(mqtt_client):
    # print("returning to base")
    mqtt_client.send_message("return_home")


def detect(mqtt_client):
    mqtt_client.send_message("detector")

def status():
    global is_stopped
    print(is_stopped)
    is_stopped = False

def main():

    root = tk.Tk()

    canvas = tk.Canvas(master=root, width=505, height=505)
    canvas.pack()

    t = turtle.RawTurtle(canvas)
    photo = tk.PhotoImage(file="ldr4.png")
    canvas.create_image(0, 0, image=photo)
    t.pencolor('#ae943d')
    t.pensize(10)
    t.penup()
    t.pendown()

    root.bind('<Up>', lambda event: forward(mqtt_client, t))
    root.bind('<Down>', lambda event: back(mqtt_client, t))
    root.bind('<Left>', lambda event: left(mqtt_client, 90, t))
    root.bind('<Right>', lambda event: right(mqtt_client, 90, t))
    root.bind('<d>', lambda event: detect(mqtt_client))
    root.bind('<space>', lambda event: stop(mqtt_client))
    root.bind('<Escape>', lambda event: return_home(mqtt_client))
    root.bind('<r>', lambda event: status())

    root.mainloop()


mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()
is_stopped = False
main()
