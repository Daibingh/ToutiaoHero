# coding:utf-8

import subprocess
import time
import cv2
import numpy as np
from utils import run_time, ocr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import PyHook3 as pyHook
import pythoncom
import sys


hot_key = "F2"
search_engine = 'http://www.baidu.com'
chromedriver_path = './chromedriver_win32/chromedriver.exe'

@run_time
def screencap():
    cmd = conf.cmd
    ret = subprocess.call(cmd, shell=True, timeout=3)
    return ret

@run_time
def crop_img(folder):
    img_file = folder+'screen.png'
    img = cv2.imread(img_file)
    x, y, w, h = conf.roi
    img = img[y:y+h,x:x+w]
    return cv2.imwrite(folder+'screen_croped.png', img)

@run_time
def process_res(res):
    text = ' '.join([t.get('words').strip() for t in res])
    # que_opt = text[2:].split('?')
    # que_opt[0] += '?'
    ind = text.find('.')
    return text[ind+1:]


def main():
    ret = screencap()
    res = ''
    if ret != 0:
        print('\033[1;31m---- adb offline!\033[0m')
        return
    try:
        crop_img(conf.img_folder)
        res = ocr(conf.img_folder+'screen_croped.png')
        res = process_res(res)
        print(">>>> 搜索的关键词是：{}".format(res))
        elem = browser.find_element_by_id("kw")
        elem.clear()
        elem.send_keys(res)
        elem.send_keys(Keys.RETURN)
    except Exception as e:
        print('\033[1;31m---- parsing error!\033[0m')


def test():
    res = '啊哈哈哈哈哈哈哈哈哈哈'
    print(">>>> 搜索的关键词是：{}".format(res))
    elem = browser.find_element_by_id("kw")
    elem.clear()
    elem.send_keys(res)
    elem.send_keys(Keys.RETURN)


def onKeyboardEvent(event):
    if event.Key == 'F2':
        # test()
        main()
    elif event.Key == 'Q':
        browser.quit()
        sys.exit()
    return True


if __name__ == '__main__':

    if sys.argv[1] == '1':
        from config import conf1 as conf  # 手机配置
        subprocess.call('adb devices', shell=True)
    elif sys.argv[1] == '2':
        from config import conf2 as conf
        subprocess.call('adb connect 127.0.0.1:62001', shell=True)
        subprocess.call('adb devices', shell=True)

    browser = webdriver.Chrome(chromedriver_path)
    browser.get(search_engine)

    # 创建管理器
    hm = pyHook.HookManager()
    # 监听键盘
    hm.KeyDown = onKeyboardEvent   
    hm.HookKeyboard()  
    # 循环监听
    pythoncom.PumpMessages()
