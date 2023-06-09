# Robot_Arm_

## Introduction

This part should give a general introduction to your project.

We planned, developed and managed a software project using agile scrum technices. The problem we tacled was that workers at a warehouse injured themselves when sorting packages based on their type. The solution is to use robots to sort the packages based on different properties. Using a lego robot arm we created software that sorted different legos by colour in different ways. The robots are equipped with motors and sensors to enable them to recognize, pick and place items. The environment of which the robots operate in
has been marked with lines to indicate where the robots operate without the possibility of injuring a human.


## Getting started

This section is supposed to guide a new developer through the steps of how to set up the project and install the deppendencies they need to start developing.
Download and flash the EV3 MicroPython image onto a micro SD card Insert your micro SD card into the SD card slot on the EV3 Brick and turn it on Download, install, and launch the free Visual Studio Code editor on your computer. Install and activate the LEGO Education EV3 extension, Connect the EV3 Brick to your computer and use the code provided. 
For more information visit https://pybricks.com/install/mindstorms-ev3/installation/

## Building and running

This is where you explain how to make the project run. What is your startup procedure? Does the program accept different arguments to do different things?

You should also describe how to operate your program. Does it need manual input before it starts picking up and sorting the items?

- Pair the two robots with Bluetooth
- Start the program on both robots and wait for the robots to finish the startup procedure
- Set one robot as server, then the other as client
- Set the pick-up zone and drop-off zones for the client robot
    - Move the robot arm with the buttons on the robot
    - Important: before you press to set a drop-off zone, place a brick with the color you want to set the drop-off for at the pick-up zone
- Set the pick-up zone and drop-off zones for the server robot the same way
- The server robot will check the pick-up zone every 5 seconds and the robots will work together to put the bricks at their correct locations


## Features

- [x] US_1: As a customer, I want the robot to pick up items from a designated position.
- [x] US_2: As a customer, I want the robot to drop off items at a designated postion.
- [x] US_3: As a customer, I want the robot to be able to determine if an item is present at a given location.
- [x] US_4: As a customer, I want the robot to tell me the color of an item at a designated position.
- [x] US_5: As a customer, I want the robot to drop items off at different locations based on the color of the item.
- [x] US_6: As a customer, I want the robot to be able to pick up items from elevated positions.
- [x] US_7: As a customer, I want to be able to calibrate maximum of three different colors and assign them to specific drop-off zones based on color.
- [x] US_9: As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived.
- [x] US_10: As a customer, I want the robots to sort items at a specific time.
- [x] US_11: As a customer, I want two robots to communicate and work together on items sorting without colliding with each other.
- [x] US_12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by using buttons)
