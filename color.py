import numpy as np
import argparse
import cv2
image = cv2.imread('1.save')


def filter_out_red():
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    # inRange()方法返回的矩阵只包含0,1 0表示不在区间内
    mask = cv2.inRange(image, lower_red, upper_red)
    output = cv2.bitwise_and(image, image, mask = mask)

    # 展示图片
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)

filter_out_red()
