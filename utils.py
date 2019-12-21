# coding:utf-8

import time
from aip import AipOcr
import logging
import subprocess
import requests as R
import json
from os.path import dirname, join


with open(join(dirname(__file__), "baidu_ocr.json"), 'r') as f:
    j = json.load(f)

client = AipOcr(j['APP_ID'], j['API_KEY'], j['SECRET_KEY'])


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

@run_time
def crop_ocr(img_file):
    cmd = './bin/crop_ocr {}'.format(img_file)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return json.loads(p.stdout.read())['words_result']

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