import cv2
import numpy as np
from scipy.stats import norm

digit_vecs = np.loadtxt('./digit_vecs.txt')

def recognize(p_img):
    img = cv2.imread(p_img)
    gray = img[:,:,2].astype(int)
    gray[gray<255] = -1
    gray[gray>=255] = 1
    
    img_1 = gray[7:-7:,5:13]
    img_2 = gray[7:-7,14:22]
    img_3 = gray[7:-7,45:53]
    img_4 = gray[7:-7,54:62]
    
    num_1 = recognize_digit(img_1)
    num_2 = recognize_digit(img_2)
    num_3 = recognize_digit(img_3)
    num_4 = recognize_digit(img_4)
    
    if num_2 == 10:
        x_1 = num_1
    else:
        x_1 = num_1 * 10 + num_2
        
    if num_4 == 10:
        x_2 = num_3
    else:
        x_2 = num_3 * 10 + num_4
        
    he = x_1 + x_2
    return he
    
def recognize_digit(seg_img):
    seg_img_flat = seg_img.flatten()
    seg_img_flat = seg_img_flat.flatten()/np.linalg.norm(seg_img_flat)
    
    num = np.argmax(np.dot(digit_vecs, seg_img_flat))
    return num



