import cv2
import numpy as np

# Incarca imaginea desenului
imagine = cv2.imread('../test_files/floare.jpeg')

# Converteste imaginea in grayscale
imagine_gri = cv2.cvtColor(imagine, cv2.COLOR_BGR2GRAY)

# Aplicare binarizare
imagine_binar = cv2.threshold(imagine_gri, 127, 255, cv2.THRESH_BINARY)[1]

# Gasirea contururilor
contururi, _ = cv2.findContours(imagine_binar, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initializare lista de coordonate
coordonate = []

# Iterare prin contururi
for contur in contururi:
    # Aproximare contur cu linii drepte
    aproximare = cv2.approxPolyDP(contur, 0.01 * cv2.arcLength(contur, True), True)

    # Adaugarea coordonatelor varfurilor la lista
    for punct in aproximare:
        coordonate.append(punct[0])

# Transformarea in formatul dorit
coordonate_formatate = []
for i in range(0, len(coordonate), 2):
    coordonate_formatate.append((coordonate[i], coordonate[i + 1]))

# Afisarea coordonatelor
print("Coordonatele desenului:")
print(coordonate_formatate)

# Desenați coordonatele pe imagine
for punct in coordonate_formatate:
    # cv2.circle(imagine, punct, 3, (0, 255, 0), -1)

    cv2.circle(imagine, (punct[0][0], punct[0][1]), 3, (0, 255, 0), -1)


# Afisarea imaginii cu punctele marcate
cv2.imshow('Desen cu puncte marcate', imagine)
cv2.waitKey(0)
