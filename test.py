import cv2
import numpy as np

a = cv2.imread(("OCR1.png"), cv2.IMREAD_GRAYSCALE)

print(a.shape)

print(a)
def bilinear_interpolate(gray_np_image, np_p00, np_p10, np_p01, np_p11):
    ans_image = np.zeros((max(np_p00[0], np_p10[0], np_p01[0], np_p11[0]), max(np_p00[1], np_p10[1], np_p01[1], np_p11[1])))
    