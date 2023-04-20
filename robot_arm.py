#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

ev3 = EV3Brick()
gripper_motor = Motor(Port.A)
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)
touch_sensor = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)

base_motor.run(-60)
while not touch_sensor.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)
elbow_motor.run_until_stalled(-30,then=Stop.BRAKE,duty_limit=20)
wait(10)
elbow_motor.reset_angle(0)
elbow_motor.run_target(60,61.5)
elbow_motor.reset_angle(0)


def pick_up(position):
    #move claw to position
    base_motor.run_target(135, position)

    elbow_motor.run_target(60,-29)
    gripper_motor.run_until_stalled(200,then=Stop.HOLD, duty_limit=50)
    elbow_motor.run_target(60,0)


def read_color():
    rgb = color_sensor.rgb()
    return rgb_to_color(rgb)

def rgb_to_color(rgb):
    if rgb[0] > (rgb[1] + rgb[2]) / 2:
        if (rgb[0] - rgb[1]) < 8 and rgb[1] > 2:
            return "YELLOW"
        return "RED"
    elif rgb[1] > (rgb[0] + rgb[2]) / 2:
        return "GREEN"
    elif rgb[2] > (rgb[0] + rgb[1]) / 2:
        return "BLUE"
    return "None"


def drop(position):
    #move claw to position
    base_motor.run_target(135, position)
    elbow_motor.run_target(60,-29)

    #drop brick
    gripper_motor.run_target(200,-90)

    #reset claw position
    elbow_motor.run_target(60,0)


def is_present(position):
    #try to pick up item at position
    pick_up(position)

    angle = int(gripper_motor.angle())

    drop(position)

    #claw positions:
    #-31.5 when holding item
    #-4 when empty
    if angle < -10:
        return True
    return False

color_pos = {
    "YELLOW": 90,
    "RED": 130,
    "GREEN": 170,
    "BLUE": 210
}

while True:
    up = int(input("Pick up at position: "))
    pick_up(up)
    color = read_color()
    print(color)
    drop(color_pos[color])
    # print("Claw position: " + str(gripper_motor.angle()))
    # down = int(input("Drop at position: "))
    # drop(down)