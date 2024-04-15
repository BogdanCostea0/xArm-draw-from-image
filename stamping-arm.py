'''
from tkinter import *


def fiir_stamp():
    choice = 1
    return choice

def rsp_stamp():
    choice = 2
    return choice 

def spd_stamp():
    choice = 3
    return choice

def fiirbots_stamp():
    choice = 4
    return choice

    # =================================[UI]==============================
    

GRAY = "#d3d3d3"
GREEN = "#9bdeac"
BLUE = "#154c79"
FONT_NAME = "Courier"


window = Tk()
window.title("Get yout stamp - FIIRBots")
window.config(padx=40,pady=40,bg=GRAY, highlightthickness=0)

canvas = Canvas(width=400, height=400,bg=GRAY)

my_label = Label(text="Get your stamp - FIIRBOTS", font=("Arial", 24), background=GRAY) 
my_label.grid(column=1  , row=1)

# creare buton de fiir
fiir = Button(text="FIIR STAMP", command=fiir_stamp)
fiir.config(width=15)
fiir.grid(column=0,row=3)

# creare buton de rsp
rsp = Button(text="RSP STAMP", command=rsp_stamp)
rsp.config(width=15)
rsp.grid(column=1,row=3)

# creare buton de spd
spd = Button(text="SPD STAMP", command=spd_stamp)
spd.config(width=15)
spd.grid(column=2,row=3)

# creare buton de fiirbots
FIIRBots = Button(text="FIIRBots STAMP", command=fiirbots_stamp)
FIIRBots.config(width=15)
FIIRBots.grid(column=1,row=5)

window.mainloop()
'''

# =================================[ROBOT MOVEMENT]==========================

import os
import sys
choice = input("Alege varianta. 1- FIIRBots, 2 - RSP, 3 - SPD, 4 - FIIRBots:      ")

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



if int(choice) == 1:
    # go to grab stamp 
    yStamp = 0
elif int(choice) == 2:
    yStamp = 40
elif int(choice) == 3:
    yStamp = 80
elif int(choice) == 4:
    yStamp = -40
    
# go to grab stamp 
arm.set_position(x=100, y=yStamp, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=100, y=yStamp, z=GRAB_HEIGHT, wait=True, speed=50)
arm.set_position(x=100, y=yStamp, z=UP_HEIGHT, wait=True,speed=150)

# go to ink
arm.set_position(x=250, y=0, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=250, y=0, z=GRAB_HEIGHT, wait=True,speed=50)
arm.set_position(x=250, y=0, z=UP_HEIGHT, wait=True,speed=150)

# go to stamp flyer
arm.set_position(x=350, y=0, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=350, y=0, z=GRAB_HEIGHT, wait=True,speed=50)
arm.set_position(x=350, y=0, z=UP_HEIGHT, wait=True,speed=150)

# go to leave stamp 
arm.set_position(x=150, y=yStamp, z=UP_HEIGHT, wait=True,speed=150)
arm.set_position(x=150, y=yStamp, z=GRAB_HEIGHT, wait=True, speed=50)
arm.set_position(x=150, y=yStamp, z=UP_HEIGHT, wait=True,speed=150)


arm.reset()
arm.disconnect()