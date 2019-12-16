# coding:utf-8

import time
from aip import AipOcr


""" 你的 APPID AK SK """
APP_ID = '18027270'
API_KEY = 'wxHR7dilrzB3ka2M6QZrDbPp'
SECRET_KEY = 'q9gMZgoLcT9KWhx0VUG7phLkr8qaWlXu'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def run_time(func):
    def wrapper(*args, **kw):
        t0 = time.time()
        res = func(*args, **kw)
        print("---- {} elapsed: {:.3f}s".format(func.__name__, time.time()-t0))
        return res
    return wrapper

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

@run_time
def ocr(img_file):
    image = get_file_content(img_file)
    options = {}
    options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["probability"] = "true"
    res = client.basicGeneral(image, options)
    return res['words_result']