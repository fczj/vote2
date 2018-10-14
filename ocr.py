from PIL import Image
from pytesser3 import *

img = Image.open('1.save')
img_grey = img.convert('L')
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
img_out = img_grey.point(table, '1')
img_out.show()
print(image_to_string(img_out))
