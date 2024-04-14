import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import splprep, splev

# Load the image
im_cv = cv2.imread("../test_files/house.png", cv2.IMREAD_GRAYSCALE)

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

    # Increment line counter
    line_counter += 1

plt.axis('equal')
plt.gca().invert_yaxis()
plt.axis('off')
plt.show()

# Print the total number of lines used
print(f"Total lines used: {line_counter}")