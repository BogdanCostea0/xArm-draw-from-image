# ======================[ GENERATE POINTS]============================
import numpy as np
import matplotlib.pyplot as plt
import cv2


image = cv2.imread("./test_files/3_lines.png")

# convert to grayscale
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform edge detection
edges = cv2.Canny(grayscale, 30, 100)

# detect lines in the image using hough lines technique
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, np.array([]), 80, 40)

for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)

plt.imshow(image)
plt.show()

# =================================[ROBOT MOVEMENT]==========================

import os
import sys

WRITE_HEIGHT = 10 # drawing level
SAFE_HEIGHT = 30 # used to retreat after drawing a line
MAGIC_NUMBER = 0.3 # used as a scale factor
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
print(f' Number of lines: {len(lines)}')

for line in lines:
    for x1,y1,x2,y2 in line:
        # goes to the line start
        print(f'Go to X:{x1 * MAGIC_NUMBER + OFFSET}  Y:{y1 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        arm.set_position(x=x1 * MAGIC_NUMBER + OFFSET, y=y1 * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)

        # draw the line till the end
        print(f'Drawing line to X:{x2 * MAGIC_NUMBER + OFFSET}  Y:{y2 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        arm.set_position(x=x2 * MAGIC_NUMBER + OFFSET, y=y2 * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)

        # retreat to a safe zone, Z level is changed to SAFE_HEIGHT
        print(f'Retreat to safe level X:{x2 * MAGIC_NUMBER + OFFSET}  Y:{y2 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        arm.set_position(x=x2 * MAGIC_NUMBER+OFFSET, y=y2 * MAGIC_NUMBER, z=SAFE_HEIGHT, wait=True)


arm.reset(wait=True)

arm.disconnect()
