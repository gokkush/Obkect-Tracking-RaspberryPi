import sys
import numpy as np
import cv2

blue = 255
green = 104
red = 0

color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

hue = hsv_color[0][0][0]

print("Alt Sınır :"),
print("[" + str(hue - 10) + ", 100, 100]\n")

print("Üst Sınır :"),
print("[" + str(hue + 10) + ", 255, 255]")