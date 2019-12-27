# coding:utf-8

import time
from aip import AipOcr
import logging
import subprocess
import requests as R
import json
import cv2
import numpy as np
from os.path import dirname, join
from PIL import ImageFont
import jieba.posseg as pseg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re


with open(join(dirname(__file__), "baidu_ocr.json"), 'r') as f:
    j = json.load(f)

client = AipOcr(j['APP_ID'], j['API_KEY'], j['SECRET_KEY'])

neg_keywords = ['不正确',
                '不属于',
                '不准确',
                '不包含',
                '不可能',
                '不会',
                '不是']

stop_words = set(['下列',
                  '关于',
                  '有关',
                  '不'])

def isNeg(que):
    for t in neg_keywords:
        if t in que: return True
    return False


def isStable(que, score):
    score = np.asarray(list(score.values()))
    neg = isNeg(que)
    # cond = score.sum() == 0 or (neg and np.where(score==score.min())[0].shape[0]>1)
    cond = (neg and np.where(score==score.min())[0].shape[0]>1) or (not neg and np.where(score==score.max())[0].shape[0]>1)
    if cond:
        return False
    return True


class Logger:
    
    def __init__(self, file_name):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        file_handler = logging.FileHandler(file_name, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
    
    def info(self, msg):
        self._logger.info(msg)

    @property
    def disabled(self):
        return self._logger.disabled

    @disabled.setter
    def disabled(self, b):
        self._logger.disabled = b
    


def run_time(func):
    def wrapper(*args, **kw):
        t0 = time.time()
        res = func(*args, **kw)
        print("---- {} elapsed: {:.3f}s".format(func.__name__, time.time()-t0))
        return res
    return wrapper


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

@run_time
def ocr2(img_bytes):
    options = {}
    options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["probability"] = "true"
    res = client.basicGeneral(img_bytes, options)
    return res['words_result']

# @run_time
# def crop_ocr(img_file):
#     cmd = './bin/crop_ocr {}'.format(img_file)
#     p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     return json.loads(p.stdout.read())['words_result']


@run_time
def screencap(dev='pc'):
    if dev == 'phone':
        p = subprocess.Popen('adb -s 35826afb0704 shell screencap -p', stdout=subprocess.PIPE)
        b = p.stdout.read().replace(b'\r\n', b'\n')
    else:
        p = subprocess.Popen('adb shell screencap -p', stdout=subprocess.PIPE)
        b = p.stdout.read().replace(b'\r\r\n', b'\n')
    return cv2.imdecode(np.asarray(bytearray(b), dtype=np.uint8), cv2.IMREAD_COLOR)


@run_time
def crop_img(img, roi, th=-1):
    x, y, w, h = roi
    img = img[y:y+h,x:x+w]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if th > 0: _, img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)
    _, buf = cv2.imencode(".png", img)
    return bytes(buf)

# @run_time
def process_res(res):
    text = ' '.join([t.get('words').strip() for t in res])
    # que_opt = text[2:].split('?')
    # que_opt[0] += '?'
    ind = text.find('.')
    if ind>2: ind = -1
    return text[ind+1:]


def baidu_browser_init(chromedriver_path):
    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    browser = webdriver.Chrome(chromedriver_path, options=option)
    browser.get('http://www.baidu.com')
    return browser


def get_text_width(text):
    font = ImageFont.truetype('arial.ttf', 1)
    return font.getsize(text)[0]+text.count(' ')

# def adjust_search_que(que, limit):
#     if get_text_width(que)<=limit:
#         return que 
#     cuts = pseg.cut(que)
#     que =''.join( [pair.word for pair in cuts if pair.flag[0]!='u' and pair.flag not in ['p','y','r','c','e']] )
#     if get_text_width(que)<=limit:
#         return que
#     return que[get_text_width(que)-limit:]

def adjust_search_que(que, limit):
    if get_text_width(que)<=limit:
        return que
    cuts = pseg.cut(que)
    que = ''
    f = False
    for pair in cuts:
        if pair.word in ['"', '“', '《'] and not f:
            f = True
        elif pair.word in ['"', '”', '》']:
            f = False
        if f: 
            que += pair.word
        elif pair.flag[0]!='u' and pair.flag not in ['p','y','r','c','e'] and pair.word not in stop_words:
            que += pair.word
    if get_text_width(que)<=limit:
        return que
    return que[get_text_width(que)-limit:]

def baidu_search(browser,search_text):
    elem = browser.find_element_by_id("kw")
    elem.clear()
    elem.send_keys(search_text)
    elem.send_keys(Keys.RETURN)

# @run_time
def baidu_score(browser, opts, que=None, cut='later_cut'):
    # res_list = browser.find_elements_by_css_selector("div.result.c-container")
    # text = '\n'.join([t.text.split('...')[0] for t in res_list])
    text = browser.find_element_by_css_selector("#content_left").text
    text = re.sub(r"更多关于.*?的问题>>", '', text)
    if cut != 'cut':
        counts = dict(zip(opts, map(lambda t: text.count(t), opts)))
        if cut == 'no_cut' or (cut == 'later_cut' and sum(counts.values())>0):
            return counts
    if cut in ['cut', 'later_cut']:
        counts = {}
        que_words = [pair.word for pair in pseg.cut(que)]
        for opt in opts:
            cuts = pseg.cut(opt)
            counts[opt] = sum([text.count(pair.word) for pair in pseg.cut(opt) 
                if pair.word not in que_words and pair.flag[0] != 'u' and pair.flag not in ['x', 'w', 'p', 'r', 'c']])
        return counts

# @run_time
def sogou_score(browser, opts):
    text = browser.find_element_by_class_name('results').text
    return dict(zip(opts, map(lambda t: text.count(t), opts)))


def parse_json(j):
    text = ''
    for d in j['data']:
        try:
            text += d['display']['summary']['text'] + '\n'
        except:
            pass
    return text

@run_time
def toutiao_score(search_text):
    opts = search_text.split('?')[-1].strip().split(' ')
    headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'    }

    params = {
            "keyword": search_text,
            'format': 'json',
            'offset': 0,
            'count': 20,
    }
    res = R.get('https://www.toutiao.com/api/search/content/', params=params, headers=headers, timeout=2)
    text = parse_json(res.json())
    return {t: text.count(t) for t in opts}