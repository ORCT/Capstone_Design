import numpy as np
import cv2

a = cv2.imread(("OCR1.png"), cv2.IMREAD_GRAYSCALE)
print(a.shape)
print(a[3, 5])

z = np.zeros((100, 100))

p1 = (10, 3)
p2 = (80, 7)
p3 = (15, 90)
p4 = (100, 100)

def lll(_a, _z, _p1, _p2, _p3, _p4):
    for i in range(1000):
        for j in range(1000):
            u = i / 1000
            v = j / 1000
            x, y = round((1 - u) * _p1[1])
             = _a[round(_a.shape[0] * u)][round(_a.shape[1] * v)]