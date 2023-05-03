#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
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
elbow_motor.run_target(60,57)
elbow_motor.reset_angle(0)


def pick_up(position):
    #move claw to position
    base_motor.run_target(135, position[0])

    #pick up
    elbow_motor.run_target(60, position[1])
    gripper_motor.run_until_stalled(200,then=Stop.HOLD, duty_limit=50)
    elbow_motor.run_target(60,0)


def read_color():
    rgb = color_sensor.rgb()
    return rgb_to_color(rgb)

def rgb_to_color(rgb):
    if rgb[0] > (rgb[1] + rgb[2]) / 2:
        if (rgb[1] >= rgb[0] / 4) and rgb[1] > 1:
            return "YELLOW"
        return "RED"
    elif rgb[1] + 1 > (rgb[0] + rgb[2]) / 2:
        return "GREEN"
    elif rgb[2] > (rgb[0] + rgb[1]) / 2:
        return "BLUE"
    return "None"

def check_color_at(position):
    pick_up(position)
    color = read_color()
    drop(position)
    return color


def drop(position):
    #move claw to position
    base_motor.run_target(135, position[0])
    elbow_motor.run_target(60, position[1])

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


pick_up_locations = [(0, 0)]
drop_off_locations = {}


def move_arm():
    #reset arm
    elbow_motor.run_target(60, 0)
    base_motor.run_target(135, 0)
    ev3.screen.draw_text(25, 50, "Move arm")

    #move arm
    while True:
        pressed = ev3.buttons.pressed()
        if Button.LEFT in pressed:
            base_motor.run(45)
        elif Button.RIGHT in pressed:
            base_motor.run(-45)
        elif Button.UP in pressed:
            elbow_motor.run(15)
        elif Button.DOWN in pressed:
            elbow_motor.run(-15)
        elif Button.CENTER in pressed:
            break
        else:
            base_motor.brake()
            elbow_motor.brake()

    #save arm position
    pos = base_motor.angle()
    hgt = elbow_motor.angle()

    #reset arm
    elbow_motor.run_target(60, 0)
    base_motor.run_target(135, 0)

    return (pos, hgt)

def set_pick_up():
    print("Set pick-up with buttons...")
    pick_up_locations[0] = move_arm()
    print("Pick-up: " + str(pick_up_locations[0]) + "\n")

def set_drop_off():
    #max 3
    if len(drop_off_locations) >= 3:
        return
    
    color = input("Input color: ")
    print("Set drop-off for " + color + " with buttons...")
    drop_off_locations[color] = move_arm()
    print("Drop-off for " + color + ": " + str(drop_off_locations[color]) + "\n")


def setup_pickup_dropoffs():
    set_pick_up()
    set_drop_off()
    set_drop_off()


#--------------------------------------------


# setup_pickup_dropoffs()

# while True:
#     input("Press enter to pick up")
#     pick_up(pick_up_locations[0])
#     drop(drop_off_locations[read_color()])
#     print()

# pos = int(input("Check at pos: "))
# hgt = int(input("Check at height: "))
# print(is_present((pos, hgt)))