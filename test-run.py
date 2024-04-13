# ======================[ GENERATE POINTS]============================
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image using OpenCV.
im_cv = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)

# Use morphological operations to clean up the edges and reduce double lines to single lines.

# Apply GaussianBlur to reduce noise and improve edge detection.
blurred = cv2.GaussianBlur(im_cv, (5, 5), 0)

# Use a threshold to clean the image further before edge detection.
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Increase the size of the kernel for more aggressive dilation and erosion to merge lines closer together.
kernel = np.ones((3, 3), np.uint8)  # Increase kernel size for more aggressive morphological operations.
dilated = cv2.dilate(thresh, kernel, iterations=2)  # Increase iterations if needed.
eroded = cv2.erode(dilated, kernel, iterations=1)  # Possibly reduce iterations to avoid over-thinning.

# Detect edges again using the Canny algorithm after morphological operations.
edges_optimized = cv2.Canny(eroded, threshold1=50, threshold2=150)

# Find coordinates of these edges.
y_coords_optimized, x_coords_optimized = np.where(edges_optimized > 0)

# Define scaling factors based on the robot's workspace and image dimensions
scale_x = 297    / 1080
scale_y = 210 / 1080
offset_x = 10 # Offset to position the drawing correctly in the robot's workspace
offset_y = 10
magic_coeficient = 0.3

# Convert image points to robot coordinates
robot_trajectory = []
counter = 0
for index in range(len(x_coords_optimized)):
    if index % 25 == 0:
     # Apply scaling and offset
     robot_x = int(x_coords_optimized[index] * scale_x * magic_coeficient + offset_x )

     robot_y = int(y_coords_optimized[index] * scale_y * magic_coeficient + offset_y )

     robot_z = 60 # Replace with a safe height value for the robot to move in

     # Add the point to the trajectory
     robot_trajectory.append((robot_x, robot_y, robot_z))
     counter += 1


for each_pair_of_coord in robot_trajectory:
    print(f'X: {each_pair_of_coord[0]} | Y: {each_pair_of_coord[1]} | Z: {each_pair_of_coord[2]} ')


print(f'Total lenght of robot traj: {len(robot_trajectory)}')

# =================================[ROBOT MOVEMENT]==========================

import os
import sys
import time
import math

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

speed = 50

for eachPairOfCoords in robot_trajectory:
    arm.set_position(x=each_pair_of_coord[0], y=each_pair_of_coord[1], z=each_pair_of_coord[2], wait=True)
    print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))


# arm.reset(wait=True)

arm.disconnect()

