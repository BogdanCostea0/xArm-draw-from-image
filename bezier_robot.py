import cv2
import numpy as np
import matplotlib.pyplot as plt

# Citirea imaginii
image = cv2.imread('./test_files/floare.jpeg')

# Convertirea imaginii la tonuri de gri
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detectarea marginilor folosind Canny Edge Detection
edges = cv2.Canny(gray, 30, 200)

# Găsirea contururilor
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Crearea unui canvas gol pentru a desena conturul
contour_image = np.zeros_like(gray)

# Desenarea tuturor contururilor
cv2.drawContours(contour_image, contours, -1, (255), thickness=cv2.FILLED)

# Extrage coordonatele punctelor din contur pentru fiecare contur
all_contour_pts = [np.squeeze(contour) for contour in contours]

# Interpolarea curbelor Bezier
def bezier_curve(p0, p1, p2, p3, t):
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3

# Desenarea curbelor Bezier pentru fiecare contur
def draw_bezier_curve(pts, num_points=100):
    for i in range(len(pts) - 3):
        curve_points = []
        for t in np.linspace(0, 1, num_points):
            point = bezier_curve(pts[i], pts[i+1], pts[i+2], pts[i+3], t)
            curve_points.append(point)
        curve_points = np.array(curve_points)
        plt.plot(curve_points[:, 0], curve_points[:, 1], color='blue')



# Desenarea imaginii și a tuturor contururilor
plt.figure(figsize=(8, 8))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
for contour_pts in all_contour_pts:
    draw_bezier_curve(contour_pts)
plt.axis('off')
plt.show()


# =================================[ROBOT MOVEMENT]==========================

import os
import sys

WRITE_HEIGHT = 20 # drawing level
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

speed = 500


counter = 0
for contour_pts in all_contour_pts:
    for pt in contour_pts:
        counter += 1
        print(f'Go total {counter} / {len(all_contour_pts)} to X:{pt[0] * MAGIC_NUMBER + OFFSET}  Y:{pt[1] * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        arm.set_position(x=pt[0] * MAGIC_NUMBER + OFFSET, y=pt[1] * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)
        # print(f'Retreat to safe level X:{pt[0]* MAGIC_NUMBER + OFFSET}  Y:{pt[1] * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        # arm.set_position(x=pt[0] * MAGIC_NUMBER+OFFSET, y=pt[1] * MAGIC_NUMBER, z=SAFE_HEIGHT, wait=True)


# for line in lines:
#     for x1,y1,x2,y2 in line:
#         counter += 1
#         # goes to the line start
#         print(f'Go to X:{x1 * MAGIC_NUMBER + OFFSET}  Y:{y1 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
#         arm.set_position(x=x1 * MAGIC_NUMBER + OFFSET, y=y1 * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)
#
#         # draw the line till the end
#         print(f'Drawing line {counter} / {len(lines)}  to X:{x2 * MAGIC_NUMBER + OFFSET}  Y:{y2 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
#         arm.set_position(x=x2 * MAGIC_NUMBER + OFFSET, y=y2 * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)
#
#         # retreat to a safe zone, Z level is changed to SAFE_HEIGHT
#         print(f'Retreat to safe level X:{x2 * MAGIC_NUMBER + OFFSET}  Y:{y2 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
#         arm.set_position(x=x2 * MAGIC_NUMBER+OFFSET, y=y2 * MAGIC_NUMBER, z=SAFE_HEIGHT, wait=True)


arm.reset(wait=True)

arm.disconnect()
