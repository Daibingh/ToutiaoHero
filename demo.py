# coding:utf-8

import subprocess
import time
import cv2
import numpy as np
from utils import run_time, ocr, Logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import PyHook3 as pyHook
import pythoncom
import sys
import shutil
import uuid


hot_key = "F2"
search_engine = 'http://www.baidu.com'
chromedriver_path = './chromedriver_win32/chromedriver.exe'
log = Logger('log.txt')

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


def move_image(dist_folder, uid):
    shutil.move(conf.img_folder+'screen.png', dist_folder+uid+'.png')  # 移动文件
    shutil.move(conf.img_folder+'screen_croped.png', dist_folder+uid+'_croped.png')


def baidu_score(browser, opts):
    res_list = browser.find_elements_by_css_selector("div.result.c-container")
    text = ' '.join([t.text.split('...')[0] for t in res_list]).replace('\n', ' ')
    return dict(zip(opts, map(lambda t: text.count(t), opts)))


def main():
    uid = uuid.uuid4().hex
    ret = screencap()
    if ret != 0:
        print('\033[1;31m---- adb offline!\033[0m')
        return
    try:
        crop_img(conf.img_folder)
        ocr_res = ocr(conf.img_folder+'screen_croped.png')
        search_text = process_res(ocr_res)
        print(">>>> 搜索的关键词是：{}".format(search_text))
        log.info("{}: {}".format(uid, search_text))
        elem = browser.find_element_by_id("kw")
        elem.clear()
        elem.send_keys(search_text)
        elem.send_keys(Keys.RETURN)
        time.sleep(0.2)
        opt_score = baidu_score(browser, search_text.split('?')[-1].strip().split(' '))
        print('>>>> 百度打分: {}'.format(opt_score))
        print(">>>> 百度推荐答案: {}, 备选(否定题目): {}".format(max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)))
        print('------------------------------------------------------')
        log.info("{}: 百度打分 {}".format(uid, opt_score))
    except Exception as e:
        print('\033[1;31m---- parsing error!\033[0m')
        log.info('{}: parsing error!'.format(uid))
    try:
        move_image('debug_images/', uid)
    except Exception as e:
        pass 


def test():
    res = '啊哈哈哈哈哈哈哈哈哈哈'
    print(">>>> 搜索的关键词是：{}".format(res))
    elem = browser.find_element_by_id("kw")
    elem.clear()
    elem.send_keys(res)
    elem.send_keys(Keys.RETURN)


def test2():
    search_text_list = ["2019年8月发行的新版第五套人民币没有以下 哪种面额的纸币? 100元 50元 1元",
                    "进博会吉祥物叫什么名字? 招财 进宝 来福",
                    "澳门回归时唱响的《七子之歌》的词作者是 哪个诗歌流派的? 朦胧派 新月派 湖畔派",
                    '小明来到北京大兴国际机场的餐厅用餐时,发现? 价高质低 同质同价 同质价高',
                    '以下哪个项目不属于今年举行的世界军人运动 会上的项目? 跳伞 击剑 散打',
                    '小明乘坐高铁时发现车辆正疾驰穿过航站 楼,请问他正在哪一机场附近? 北京大兴国际机场 厦门高崎国际机场 广州白云国际机场',
                    '中国女排目前已经十度成为世界冠军,其中包 含了奥运会、世界杯和哪项赛事? 国际排联大冠军杯 世俱杯 世锦赛'
                    ]
    search_text = np.random.choice(search_text_list)
    print(">>>> 搜索的关键词是：{}".format(search_text))
    elem = browser.find_element_by_id("kw")
    elem.clear()
    elem.send_keys(search_text)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    opt_score = baidu_score(browser, search_text.split('?')[-1].strip().split(' '))
    print('>>>> 百度打分: {}'.format(opt_score))
    print(">>>> 百度推荐答案: {}, 备选(否定题目): {}".format(max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)))
    print('------------------------------------------------------')


def onKeyboardEvent(event):
    if event.Key == 'F2':
        # test()
        test2()
        # main()
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
