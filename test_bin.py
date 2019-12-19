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

def crop_ocr(img_file):
    cmd = './bin/crop_ocr {}'.format(img_file)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return json.loads(p.stdout.read())['words_result']

if __name__ == '__main__':
    t0 = time.time()
    p = subprocess.Popen('./bin/crop_ocr screen.png', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    j = json.loads(p.stdout.read())
    print(j)
    print(time.time()-t0)

    t0 = time.time()
    crop_img('./')
    ocr_res = ocr('screen_croped.png')
    print(ocr_res)
    print(time.time()-t0)
