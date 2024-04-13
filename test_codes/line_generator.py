# ======================[ GENERATE POINTS]============================
import numpy as np
import matplotlib.pyplot as plt
import cv2


image = cv2.imread("../test_files/test3.png")

# convert to grayscale
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform edge detection
edges = cv2.Canny(grayscale, 50, 100)

# detect lines in the image using hough lines technique
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, np.array([]), 20, 10)

if lines is None or len(lines) < 5:
    print('No lines found')

    # detect lines in the image using contour technique
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # make sure that the contours are not empty

    # transform the contours into lines for better visualization
    lines = []
    for contour in contours:
        for i in range(len(contour) - 1):
            x1, y1 = contour[i][0]
            x2, y2 = contour[i + 1][0]
            lines.append([[x1, y1, x2, y2]])

    # reduce the number of lines by tolerance (distance between points)
    lines = np.array(lines)
    tolerance = 18
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
    new_lines = np.array(new_lines)
    lines = new_lines

    # merge lines that are close to each other
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
    new_lines = np.array(new_lines)
    lines = new_lines

    # make long lines shorter by removing the middle part
    tolerance = 10
    new_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) > tolerance:
            new_lines.append(line)
    new_lines = np.array(new_lines)
    lines = new_lines

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)
    print(f'Number of lines: {len(lines)}')

else:
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)

    print(f'Number of lines: {len(lines)}')

plt.imshow(image)
plt.show()
