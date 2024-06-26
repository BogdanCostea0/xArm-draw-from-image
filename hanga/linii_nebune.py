# ======================[ GENERATE POINTS]============================
import numpy as np
import matplotlib.pyplot as plt
import cv2


image = cv2.imread("../test_files/test3.png")

# convert to grayscale
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform edge detection
edges = cv2.Canny(grayscale, 50, 100)

# get the coordinates of the edges
y_coords, x_coords = np.where(edges > 0)

# edges to countours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# make image with contours
# image = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
lines = []
if(len(contours) > 0):
    # get x and y coordinates of the contours and create lines
    for contour in contours:
        for i in range(len(contour) - 1):
            x1, y1 = contour[i][0]
            x2, y2 = contour[i + 1][0]
            lines.append([[x1, y1, x2, y2]])

    # reduce the number of lines by merging lines that are close to each other into one line if the distance between them is less than 10 pixels

    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]
            if np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) < 10:
                lines[i][0] = [x1, y1, x4, y4]
                lines.pop(j)
                break

    # reduce lines that are shorter than a variable named pixel
    pixel = 4
    lines = [line for line in lines if np.sqrt((line[0][0] - line[0][2]) ** 2 + (line[0][1] - line[0][3]) ** 2) > pixel]

    # unite lines that are close to each other

    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]
            if np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) < 10:
                lines[i][0] = [x1, y1, x4, y4]
                lines.pop(j)
                break

    # make rounded lines with the coordinates of the lines that are close to each other and have the same slope
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]
            if np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) < 10:
                lines[i][0] = [x1, y1, x4, y4]
                lines.pop(j)
                break


    # draw lines
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)



print(len(lines))

plt.imshow(image)
plt.show()

# =================================[ROBOT MOVEMENT]==========================

import os
import sys

WRITE_HEIGHT = 7 # drawing level
SAFE_HEIGHT = 20 # used to retreat after drawing a line
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

speed = 400
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
