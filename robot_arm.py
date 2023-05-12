#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox

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
base_motor.run_target(150, 90)
base_motor.hold()

gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)
elbow_motor.run_until_stalled(-30,then=Stop.BRAKE,duty_limit=20)
wait(10)
elbow_motor.reset_angle(0)
elbow_motor.run_target(60,59)
elbow_motor.reset_angle(0)
elbow_motor.run_target(60,15)


#connect to other robot
is_server = True
ev3.screen.draw_text(0, 40, "Left: Client")
ev3.screen.draw_text(0, 65, "Right: Server")
while True:
    pressed = ev3.buttons.pressed()
    if Button.LEFT in pressed:
        is_server = False
        break
    elif Button.RIGHT in pressed:
        is_server = True
        break
ev3.screen.clear()

server = BluetoothMailboxServer()
client = BluetoothMailboxClient()

if is_server:   
    mbox = TextMailbox('greeting', server)
    server.wait_for_connection()
else:
    mbox = TextMailbox('greeting', client)
    client.connect('ev3dev')


#--------------------------------------------


def pick_up(position):
    #move claw above
    elbow_motor.run_target(60,15)

    #move claw to position
    base_motor.run_target(150, position[0])

    #pick up
    elbow_motor.run_target(60, position[1])
    gripper_motor.run_until_stalled(200,then=Stop.HOLD, duty_limit=50)
    elbow_motor.run_target(60,0)


def read_color():
    #check if block is being held
    if not is_present():
        return "None"
    
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


def drop(position): #redundant
    #move claw above
    elbow_motor.run_target(60,15)

    #move claw to position
    base_motor.run_target(150, position[0])
    elbow_motor.run_target(60, position[1])

    #drop brick
    gripper_motor.run_target(200,-90)

    #reset claw position
    elbow_motor.run_target(60,0)


def is_present():
    angle = int(gripper_motor.angle())
    if angle < -10:
        return True
    return False


pick_up_locations = [(0, 0)]
drop_off_locations = {}
amt_set = 0


def move_arm():
    #reset arm
    elbow_motor.run_target(60, 15)
    base_motor.run_target(150, 0)
    ev3.screen.draw_text(0, 50, "Move arm")

    #move arm
    while True:
        pressed = ev3.buttons.pressed()
        if Button.LEFT in pressed:
            base_motor.run(50)
        elif Button.RIGHT in pressed:
            base_motor.run(-50)
        elif Button.UP in pressed:
            elbow_motor.run(20)
        elif Button.DOWN in pressed:
            elbow_motor.run(-20)
        elif Button.CENTER in pressed:
            break
        else:
            base_motor.brake()
            elbow_motor.brake()

    #save arm position
    pos = base_motor.angle()
    hgt = elbow_motor.angle()

    #reset arm
    elbow_motor.run_target(60, 15)
    base_motor.run_target(150, 0)

    ev3.screen.clear()

    return (pos, hgt)

def set_pick_up():
    pick_up_locations[0] = move_arm()
    #default positions
    drop_off_locations["RED"] = pick_up_locations[0]
    drop_off_locations["YELLOW"] = pick_up_locations[0]
    drop_off_locations["GREEN"] = pick_up_locations[0]
    drop_off_locations["BLUE"] = pick_up_locations[0]

def set_drop_off():
    #max 3
    global amt_set
    if amt_set >= 3:
        return
    amt_set += 1

    color = check_color_at(pick_up_locations[0])
    drop_off_locations[color] = move_arm()


def setup_pickup_dropoffs():
    wait_for_press("Press: set pick-up")
    set_pick_up()
    move_clear()
    wait_for_press("Press: set drop-off")
    set_drop_off()
    wait_for_press("Press: set drop-off")
    set_drop_off()


def wait_for_press(text):
    while True:
        ev3.screen.draw_text(0, 50, text)
        if Button.CENTER in ev3.buttons.pressed():
            ev3.screen.clear()
            wait(250)
            return


def check_pick_up():
    pick_up(pick_up_locations[0])

    color = read_color()
    if (color == "None"):
        #open claw if no brick
        gripper_motor.run_target(200,-90) 
        elbow_motor.run_target(60, 15)
        return False
    
    drop_off = drop_off_locations[color]
    drop(drop_off)

    elbow_motor.run_target(60, 15)

    #give to other robot
    if drop_off == pick_up_locations[0]:
        return True
    
    return False

def move_clear():
    elbow_motor.run_target(60, 60)
    base_motor.run_target(150, 100)


#--------------------------------------------


setup_pickup_dropoffs()

if is_server:
    while True:    
        #wait_for_press("Press: pick up")
        wait(5000)
        if check_pick_up():
            move_clear()
            mbox.send('pick')
            mbox.send('')
            mbox.wait_new()
else:
    while True:
        move_clear()
        mbox.wait_new()
        check_pick_up()
        mbox.send('done')
        mbox.send('')
# while True:
#     wait(5000)
#     if check_pick_up():
#         move_clear()
