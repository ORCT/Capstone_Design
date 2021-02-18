import numpy as np
import cv2

a = cv2.imread(("OCR1.png"), cv2.IMREAD_GRAYSCALE)
print(a.shape)

z = np.zeros((100, 100, 2))

p1 = (10, 10)
p2 = (15, 90)
p3 = (80, 7)
p4 = (100, 100)

def lll(_a, _z, _p1, _p2, _p3, _p4):
    for i in range(1000):
        for j in range(1000):
            u = i / 1000
            v = j / 1000
            x = round((1 - u) * ((1 - v) * _p1[0] + v * _p2[0]) + u * ((1 - v) * _p3[0] + v * _p4[0]))
            y = round((1 - u) * ((1 - v) * _p1[1] + v * _p2[1]) + u * ((1 - v) * _p3[1] + v * _p4[1]))
            try:
                _z[x][y][0] = (_z[x][y][0] * _z[x][y][1] + _a[round(_a.shape[0] * u)][round(_a.shape[1] * v)]) / (_z[x][y][1] + 1)
                _z[x][y][1] += 1
            except:
                pass


print(a[29][79])
lll(a, z, p1, p2, p3, p4)
print(z[:, :, 0])

# _, z = cv2.threshold(z, 110, 255, cv2.THRESH_BINARY)
cv2.imwrite("asd.png", z[:, :, 0])