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

def pick_up():
    elbow_motor.run_target(60,-20)
    gripper_motor.run_until_stalled(200,then=Stop.HOLD, duty_limit=50)
    elbow_motor.run_target(60,0)


def drop(position):
    base_motor.run_target(135, position)
    elbow_motor.run_target(60,-20)
    gripper_motor.run_target(200,-90)
