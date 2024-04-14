# ======================[ GENERATE POINTS]============================
import numpy as np
import matplotlib.pyplot as plt
import cv2


image = cv2.imread("../../test_files/floare.jpeg")

# convert to grayscale
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform edge detection
edges = cv2.Canny(grayscale, 50, 100)

# get the coordinates of the edges
y_coords, x_coords = np.where(edges > 0)

# edges to countours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

lines = []

# get x and y coordinates of the contours and create lines
for contour in contours:
    x = [point[0][0] for point in contour]
    y = [point[0][1] for point in contour]
    # remove the last point because it is the same as the first point
    x.pop()
    y.pop()

    for i in range(len(x) - 1):
        lines.append([[x[i], y[i], x[i + 1], y[i + 1]]])

# remove dublicates

for i in range(len(lines) - 1):
    for j in range(i + 1, len(lines)):
        x1, y1, x2, y2 = lines[i][0]
        x3, y3, x4, y4 = lines[j][0]
        if np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) < 10:
            lines[i][0] = [x1, y1, x4, y4]
            lines.pop(j)
            break

# remove short lines
pixel = 5
lines = [line for line in lines if np.sqrt((line[0][0] - line[0][2]) ** 2 + (line[0][1] - line[0][3]) ** 2) > pixel]


# draw lines
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)



print(len(lines))

plt.imshow(image)
plt.show()
