import time
import subprocess
import json
from utils import ocr
import cv2


def crop_img(folder):
    img_file = folder+'screen.png'
    img = cv2.imread(img_file)
    x, y, w, h = (48, 200, 625, 550)
    img = img[y:y+h,x:x+w]
    return cv2.imwrite(folder+'screen_croped.png', img)

if __name__ == '__main__':
    t0 = time.time()
    ret = subprocess.call('./bin/crop_ocr screen.png screen_croped.png result.json')
    with open('result.json') as f:
        res = json.load(f)
        print(res)
    print(time.time()-t0)

    t0 = time.time()
    crop_img('./')
    ocr_res = ocr('screen_croped.png')
    print(time.time()-t0)
