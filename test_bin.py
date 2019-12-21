import time
import subprocess
import json
from utils import ocr2
import cv2
import sys


def crop_img(img_file):
    img = cv2.imread(img_file)
    x, y, w, h = 48, 200, 625, 550
    img = img[y:y+h,x:x+w]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 161, 255, cv2.THRESH_BINARY)
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 12)
    _, buf = cv2.imencode(".png", binary)
    return bytes(buf)

# def crop_ocr(img_file):
#     cmd = './bin/crop_ocr {}'.format(img_file)
#     p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     return json.loads(p.stdout.read())['words_result']

if __name__ == '__main__':

    file = sys.argv[1]

    t0 = time.time()
    img_bytes = crop_img(file)
    ocr_res = ocr2(img_bytes)
    print('****',time.time()-t0)
    print(ocr_res)

    time.sleep(2)

    t0 = time.time()
    p = subprocess.Popen('./bin/crop_ocr {}'.format(file), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    j = json.loads(p.stdout.read())
    print('****',time.time()-t0)
    print(j)