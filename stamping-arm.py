# =================================[UI]==============================
from tkinter import *

window = Tk()

window.title("Get your stamp - FIIRBots")

window.minsize(width=500, height=500)


my_label = Label(text="Te rog alege o varianta", font=("Arial", 24)) 
my_label.grid(column=0  , row=0)


window.mainloop()
# =================================[ROBOT MOVEMENT]==========================

import os
import sys

UP_HEIGHT = 100 # drawing level
GRAB_HEIGHT = 20 # used to retreat after drawing a line





OFFSET = 40
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

# CONFIG ROBOT AND IP

if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        # ip = input('Please input the xArm ip address:')
        ip = '192.168.1.160'
        if not ip:
            print('input error, exit')
            sys.exit(1)

# RESET, ACTIVATE ROBOT AND SET PARAMETERS

arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
arm.reset(wait=True)

speed = 75

# go to grab stamp 
arm.set_position(x=150, y=0, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=150, y=0, z=GRAB_HEIGHT, wait=True, speed=50)
arm.set_position(x=150, y=0, z=UP_HEIGHT, wait=True,speed=150)

# go to ink
arm.set_position(x=250, y=0, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=250, y=0, z=GRAB_HEIGHT, wait=True,speed=50)
arm.set_position(x=250, y=0, z=UP_HEIGHT, wait=True,speed=150)


# go to stamp flyer
arm.set_position(x=350, y=0, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=350, y=0, z=GRAB_HEIGHT, wait=True,speed=50)
arm.set_position(x=350, y=0, z=UP_HEIGHT, wait=True,speed=150)


# go to leave stamp 
arm.set_position(x=150, y=0, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=150, y=0, z=GRAB_HEIGHT, wait=True, speed=50)
arm.set_position(x=150, y=0, z=UP_HEIGHT, wait=True,speed=150)
# ------
# arm.set_position(x=150, y=0, z=UP_HEIGHT, wait=True,speed=150)
# arm.set_position(x=250, y=0, z=GRAB_HEIGHT, wait=True,speed=50)



'''
#---------------

# arm.set_gripper_position(300, wait=True)

arm.set_position(x=200, y=100, z=UP_HEIGHT, wait=True,speed=150)

arm.set_position(x=250, y=100, z=UP_HEIGHT, wait=True, speed=150)

# --------------

arm.set_position(x=250, y=100, z=GRAB_HEIGHT, wait=True, speed=150)

arm.set_position(x=300, y=100, z=UP_HEIGHT, wait=True, speed=150)

# ---------------

arm.set_position(x=100, y=100, z=UP_HEIGHT, wait=True, speed=150)

arm.set_position(x=100, y=100, z=GRAB_HEIGHT, wait=True, speed=150)

# arm.set_gripper_position(600, wait=True)

'''

arm.reset(wait=True)

arm.disconnect()
