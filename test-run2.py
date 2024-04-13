# ======================[ GENERATE POINTS]============================
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

robot_trajectory = []
im = plt.imread("../test.png")
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
grey = rgb2gray(im)
coordinates_np = np.argwhere(grey < 0.99)
coordinates = coordinates_np.tolist()

sorted_coordinates = pd.DataFrame({'x': coordinates_np[:, 1], 'y': coordinates_np[:, 0], 'z': 60})
sorted_coordinates.sort_values('x', inplace=True)

robot_trajectory = sorted_coordinates[['x', 'y']].values.tolist()



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
    print(f'Go to X:{eachPairOfCoords[0]}  Y:{eachPairOfCoords[1]}  Z:{eachPairOfCoords[2]}')
    arm.set_position(x=eachPairOfCoords[0], y=eachPairOfCoords[1], z=eachPairOfCoords[2], wait=True)
    # print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
    # time.sleep(0.05)

arm.reset(wait=True)

arm.disconnect()

