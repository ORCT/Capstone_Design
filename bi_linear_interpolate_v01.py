import numpy as np
import cv2


def bilinear_interpolate(_np_gray_image, _p1, _p2, _p3, _p4): # p1: ll, p2: lh, p3: hl, p4: hh
    ans = np.zeros((max(_p1[0], _p2[0], _p3[0], _p4[0]), max(_p1[1], _p2[1], _p3[1], _p4[1]), 2))
    for i in range(1000):
        for j in range(1000):
            u = i / 1000
            v = j / 1000
            x = round((1 - u) * ((1 - v) * _p1[0] + v * _p2[0]) + u * ((1 - v) * _p3[0] + v * _p4[0]))
            y = round((1 - u) * ((1 - v) * _p1[1] + v * _p2[1]) + u * ((1 - v) * _p3[1] + v * _p4[1]))
            try:
                ans[x][y][0] = (ans[x][y][0] * ans[x][y][1] + _np_gray_image[round(_np_gray_image.shape[0] * u)][round(_np_gray_image.shape[1] * v)]) / (ans[x][y][1] + 1)
                ans[x][y][1] += 1
            except:
                pass
    return ans[:, :, 0]

if __name__ == '__main__':
    image = cv2.imread(("OCR1.png"), cv2.IMREAD_GRAYSCALE)
    print(image.shape)

    p1 = (10, 10)
    p2 = (15, 90)
    p3 = (80, 7)
    p4 = (100, 100)
    print(image[29][79])
    name = bilinear_interpolate(image, p1, p2, p3, p4)

    cv2.imwrite("asd2.png", name)