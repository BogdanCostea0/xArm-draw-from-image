#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: Move Joint
"""

import os
import sys
import time
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#####################Cofig XArm, hardcoded IP #######################

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

            
########################################################

points = [[200,150], [250,125], [300,100], [350,75]]


arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# arm.reset(wait=True)

speed = 50

for eachPoint in points:
    arm.set_position(x= eachPoint[0], y=eachPoint[1], z=60, wait=True)

arm.set_position(x= 350   , y=150, z=60, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))


# arm.reset(wait=True)
arm.disconnect()    
