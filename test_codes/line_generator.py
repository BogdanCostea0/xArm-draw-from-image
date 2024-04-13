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

    for contour in contours:
        cv2.drawContours(image, [contour], -1, (20, 220, 20), 3)


if s_a_gasit:
    print(f'Total number of lines: {len(lines)}' )
else:
    print(f'Total number of lines: {len(contours)}' )

plt.imshow(image)

plt.show()
