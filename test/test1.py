import numpy as np

import cv2

# img = cv2.imread('test/test2.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.resize(img, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
# img = cv2.GaussianBlur(img, (9,9), 0)
# cv2.imwrite('test/out1.jpg', img)

img = cv2.imread('test/test2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img, 300, 500, None, 3)
cv2.imshow('Edge', edges)
 
lines = cv2.HoughLines(edges, 1, np.pi/180, 170, None, 0,0)
#임계값에 따라 나타내는 직선의 수가 달라짐
 
for i in range(0, len(lines)):
    rho = lines[i][0][0]
    theta = lines[i][0][1]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
 
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
 
cv2.imshow('res', img)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
