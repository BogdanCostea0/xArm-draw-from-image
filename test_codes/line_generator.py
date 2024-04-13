# ======================[ GENERATE POINTS]============================
import numpy as np
import matplotlib.pyplot as plt
import cv2


image = cv2.imread("../test_files/daria.jpeg")

# convert to grayscale
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform edge detection
edges = cv2.Canny(grayscale, 30, 100)

# detect lines in the image using hough lines technique
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, np.array([]), 80, 40)

s_a_gasit = True
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

try:
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)
except TypeError:

    # detect lines in the image using contour technique
    s_a_gasit = False

    # for contour in contours:
        # cv2.drawContours(image, [contour], -1, (20, 220, 20), 3)

    # transform the contours into lines for better visualization
    lines = []

    for contour in contours:
        for i in range(len(contour) - 1):
            x1, y1 = contour[i][0]
            x2, y2 = contour[i + 1][0]
            # cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)
            lines.append([[x1, y1, x2, y2]])

    # reduce the number of lines by tolerance (distance between points)
    lines = np.array(lines)
    tolerance = 10
    new_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if len(new_lines) == 0:
            new_lines.append(line)
        else:
            x1_last, y1_last, x2_last, y2_last = new_lines[-1][0]
            if np.sqrt((x1 - x1_last) ** 2 + (y1 - y1_last) ** 2) < tolerance:
                new_lines[-1][0] = [x1_last, y1_last, x2, y2]
            else:
                new_lines.append(line)
    lines = new_lines

    # reducing the number of lines by tolerance (angle between lines)
    new_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if len(new_lines) == 0:
            new_lines.append(line)
        else:
            x1_last, y1_last, x2_last, y2_last = new_lines[-1][0]
            if np.abs(np.arctan2(y2 - y1, x2 - x1) - np.arctan2(y2_last - y1_last, x2_last - x1_last)) < 0.1:
                new_lines[-1][0] = [x1_last, y1_last, x2, y2]
            else:
                new_lines.append(line)
    lines = new_lines
    lines = np.array(lines)


print(f'Total number of lines: {len(lines)}' )

# rebuild the image with the new lines
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(image, (x1, y1), (x2, y2), (20, 220, 120), 3)

plt.imshow(image)

plt.show()
