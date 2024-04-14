import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import splprep, splev

# Load the image
im_cv = cv2.imread("./test_files/test3.png", cv2.IMREAD_GRAYSCALE)

# Apply GaussianBlur
blurred = cv2.GaussianBlur(im_cv, (5, 5), 0)

# Use a threshold
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Increase the size of the kernel
kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=2)
eroded = cv2.erode(dilated, kernel, iterations=1)

# Detect contours
contours, _ = cv2.findContours(eroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Initialize counter for lines
line_counter = 0

# Initialize lists for current and next points
current_points = []
next_points = []

# Loop over the contours
for contour in contours:
    # Convert contour to numpy array
    contour_array = contour[:, 0, :]

    # Approximate the contour with Bezier curve
    tck, u = splprep([contour_array[:, 0], contour_array[:, 1]], s=1.0, per=1)
    u_new = np.linspace(u.min(), u.max(), 1000)
    x_new, y_new = splev(u_new, tck, der=0)

    # Plot the smoothed contour
    plt.plot(x_new, y_new, 'b')

    # Save the current and next points
    for i in range(len(x_new) - 1):
        current_points.append((x_new[i], y_new[i]))
        next_points.append((x_new[i + 1], y_new[i + 1]))

    # Increment line counter
    line_counter += 1

plt.axis('equal')
plt.gca().invert_yaxis()
plt.axis('off')
plt.show()

# Print the total number of lines used
print(f"Total lines used: {line_counter}")

# =================================[ROBOT MOVEMENT]==========================

import os
import sys

WRITE_HEIGHT = 8.5  # drawing level
SAFE_HEIGHT = 50  # used to retreat after drawing a line
MAGIC_NUMBER = 0.3  # used as a scale factor
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
# current_points = current_points[::50]

# reduce the number of points proportional to the number of points in the current_points list
if(len(current_points) > 100):
    current_points = current_points[::int(len(current_points)/100)]
    current_points = current_points[::2]
else:
    current_points = current_points[::2]

print(f' Number of points: {len(current_points)}')
for each in current_points:
    if (counter == 0):
        arm.set_position(x=each[0] * MAGIC_NUMBER + OFFSET, y=each[1] * MAGIC_NUMBER, z=SAFE_HEIGHT, wait=True)
    counter += 1
    print(f'[{counter} / {len(current_points)}]Go to X:{each[0] * MAGIC_NUMBER + OFFSET}  Y:{each[1] * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
    arm.set_position(x=each[0] * MAGIC_NUMBER + OFFSET, y=each[1] * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)

    # if(counter == len(points)):
    # arm.set_position(x=each[0] * MAGIC_NUMBER+OFFSET, y=each[1] * MAGIC_NUMBER, z=SAFE_HEIGHT, wait=True)


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
