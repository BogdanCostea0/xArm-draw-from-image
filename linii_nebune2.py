import cv2

# Citirea imaginii
image = cv2.imread('./test_files/daria.jpeg')

# Convertirea imaginii în gri
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Binarizarea imaginii
_, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Găsirea contururilor în imaginea binarizată
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Inițializarea listei pentru a stoca coordonatele contururilor
contour_coordinates = []

# Iterăm prin toate contururile găsite
for contour in contours:
    # Aproximăm conturul cu o precizie specificată
    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Obținem coordonatele aproximative ale conturului și le adăugăm la lista de coordonate
    for coord in approx:
        x, y = coord[0]
        contour_coordinates.append((x, y))

# Afisăm coordonatele conturului
# print("Coordonatele conturului:")
# for coord in contour_coordinates:
#     print(coord)

# obtinem linii din coordonatele conturului
lines = []
for i in range(len(contour_coordinates) - 1):
    x1, y1 = contour_coordinates[i]
    x2, y2 = contour_coordinates[i + 1]
    lines.append([[x1, y1, x2, y2]])

print("Linii:", len(lines))
for line in lines:
    print(line)


# =================================[ROBOT MOVEMENT]==========================

import os
import sys

WRITE_HEIGHT = 6.5 # drawing level
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

speed = 500
print(f' Number of lines: {len(lines)}')
counter = 0
for line in lines:
    for x1,y1,x2,y2 in line:
        counter += 1
        # goes to the line start
        print(f'Go to X:{x1 * MAGIC_NUMBER + OFFSET}  Y:{y1 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        arm.set_position(x=x1 * MAGIC_NUMBER + OFFSET, y=y1 * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)

        # draw the line till the end
        print(f'Drawing line {counter} / {len(lines)}  to X:{x2 * MAGIC_NUMBER + OFFSET}  Y:{y2 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        arm.set_position(x=x2 * MAGIC_NUMBER + OFFSET, y=y2 * MAGIC_NUMBER, z=WRITE_HEIGHT, wait=True)

        # retreat to a safe zone, Z level is changed to SAFE_HEIGHT
        print(f'Retreat to safe level X:{x2 * MAGIC_NUMBER + OFFSET}  Y:{y2 * MAGIC_NUMBER}  Z:{WRITE_HEIGHT}')
        arm.set_position(x=x2 * MAGIC_NUMBER+OFFSET, y=y2 * MAGIC_NUMBER, z=SAFE_HEIGHT, wait=True)


arm.reset(wait=True)

arm.disconnect()
