import cv2

# Citirea imaginii
image = cv2.imread('../../test_files/floare.jpeg')

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

# cream imaginea din linii
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)



# Afișăm imaginea și așteptăm tasta 'q' pentru a închide fereastra
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
