import cv2
import numpy as np
import matplotlib.pyplot as plt

# Citirea imaginii
image = cv2.imread('../../test_files/floare.jpeg')

# Convertirea imaginii la tonuri de gri
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detectarea marginilor folosind Canny Edge Detection
edges = cv2.Canny(gray, 30, 200)

# Găsirea contururilor
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Crearea unui canvas gol pentru a desena conturul
contour_image = np.zeros_like(gray)

# Desenarea tuturor contururilor
cv2.drawContours(contour_image, contours, -1, (255), thickness=cv2.FILLED)

# Extrage coordonatele punctelor din contur pentru fiecare contur
all_contour_pts = [np.squeeze(contour) for contour in contours]

# Interpolarea curbelor Bezier
def bezier_curve(p0, p1, p2, p3, t):
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3

# Desenarea curbelor Bezier pentru fiecare contur
def draw_bezier_curve(pts, num_points=100):
    for i in range(len(pts) - 3):
        curve_points = []
        for t in np.linspace(0, 1, num_points):
            point = bezier_curve(pts[i], pts[i+1], pts[i+2], pts[i+3], t)
            curve_points.append(point)
        curve_points = np.array(curve_points)
        plt.plot(curve_points[:, 0], curve_points[:, 1], color='blue')



# Desenarea imaginii și a tuturor contururilor
plt.figure(figsize=(8, 8))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
for contour_pts in all_contour_pts:
    draw_bezier_curve(contour_pts)

print("Contour points:", all_contour_pts)
plt.axis('off')
plt.show()
