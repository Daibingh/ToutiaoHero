# coding:utf-8

import subprocess
import time
import cv2
import numpy as np
from utils import run_time, ocr, Logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PyHook3 as pyHook
import pythoncom
import sys
import shutil
import uuid
from wxpy import *
import traceback
import argparse


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


def move_image(dist_folder, uid):
    shutil.move(conf.img_folder+'screen.png', dist_folder+uid+'.png')  # 移动文件
    shutil.move(conf.img_folder+'screen_croped.png', dist_folder+uid+'_croped.png')

# @run_time
def baidu_score(browser, opts):
    res_list = browser.find_elements_by_css_selector("div.result.c-container")
    text = ' '.join([t.text.split('...')[0] for t in res_list]).replace('\n', ' ')
    return dict(zip(opts, map(lambda t: text.count(t), opts)))

# @run_time
def sogou_score(browser, opts):
    text = browser.find_element_by_class_name('results').text
    return dict(zip(opts, map(lambda t: text.count(t), opts)))

@run_time
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
        print(">>>> 搜索的关键词是: {}".format(search_text))
        log.info("{}: 搜索关键词 {}".format(uid, search_text))

        browser.get('https://www.sogou.com/')
        elem = browser.find_element_by_id("query")
        elem.send_keys(search_text)
        elem.send_keys(Keys.RETURN)

        time.sleep(F.wait_time)
        WebDriverWait(browser,1,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".results")))

        opt_score = sogou_score(browser, search_text.split('?')[-1].strip().split(' '))
        sogou_ans, sogou_ans_bak = max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)

        print('>>>> 搜狗打分: {}'.format(opt_score))
        log.info("{}: 搜狗打分 {}".format(uid, opt_score))
        print('\n')
        print(">>>> 搜狗推荐答案: {}, 备选(否定题目): {}".format(sogou_ans, sogou_ans_bak))
        print('------------------------------------------------------')

        if F.use_wx:
            msg = "搜狗推荐答案: {}, 备选(否定题目): {}".format(sogou_ans, sogou_ans_bak)
            group.send(msg)

    except Exception as e:
        print('----', e)
        print(traceback.format_exc())
        log.info('{}: {}'.format(uid, e))
    try:
        if not F.no_save_img:
            move_image('debug_images/', uid)
    except Exception as e:
        print('----', e)
        print(traceback.format_exc()) 


@run_time
def test():
    search_text_list = ['从1948年的第一套人民币到如今的第五套人民 币,都是由哪家银行统一发行的? 中国银行 华北银行 中国人民银行',
                    # "进博会吉祥物叫什么名字? 招财 进宝 来福",
                    # "澳门回归时唱响的《七子之歌》的词作者是 哪个诗歌流派的? 朦胧派 新月派 湖畔派",
                    # '小明来到北京大兴国际机场的餐厅用餐时,发现? 价高质低 同质同价 同质价高',
                    '以下哪个项目不属于今年举行的世界军人运动 会上的项目? 跳伞 击剑 散打',
                    # '小明乘坐高铁时发现车辆正疾驰穿过航站 楼,请问他正在哪一机场附近? 北京大兴国际机场 厦门高崎国际机场 广州白云国际机场',
                    # '中国女排目前已经十度成为世界冠军,其中包 含了奥运会、世界杯和哪项赛事? 国际排联大冠军杯 世俱杯 世锦赛',
                    '动画片《葫芦娃》中,五娃的技能是? 隐身 吐火 吐水',
                    # '近年来备受热捧的“脏脏包"是哪一类网红商 品? 食物 箱包 洁具',
                    '00后网络聊天时经常使用的缩写“XSWL"是在 表达哪种情绪? 高兴 生气 悲伤',
                    '80年代风靡全国的“燕舞,燕舞,一曲歌来 片情″是哪种商品的广告歌曲? 收录机 电视机 卡拉OK机'
                    ]
    search_text = np.random.choice(search_text_list)
    print(">>>> 搜索的关键词是: {}".format(search_text))

    browser.get('https://www.sogou.com/')
    elem = browser.find_element_by_id("query")
    elem.send_keys(search_text)
    elem.send_keys(Keys.RETURN)

    time.sleep(F.wait_time)
    WebDriverWait(browser,1,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".results")))

    opt_score = sogou_score(browser, search_text.split('?')[-1].strip().split(' '))
    sogou_ans, sogou_ans_bak = max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)

    print('>>>> 搜狗打分: {}'.format(opt_score))
    print('\n')
    print(">>>> 搜狗推荐答案: {}, 备选(否定题目): {}".format(sogou_ans, sogou_ans_bak))
    print('------------------------------------------------------')

    if F.use_wx:
        msg = "搜狗推荐答案: {}, 备选(否定题目): {}".format(sogou_ans, sogou_ans_bak)
        group.send(msg)


def onKeyboardEvent(event):
    if event.Key == 'F2':
        if F.debug:
            test()
        else:
            main()
    elif event.Key == 'Q':
        browser.quit()
        sys.exit()
    return True


if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--use_phone', action='store_true')
    args.add_argument('--debug', action='store_true')
    args.add_argument('--use_wx', action='store_true')
    args.add_argument('--wait_time', type=float, default=.3)
    args.add_argument('--no_log', action='store_true')
    args.add_argument('--no_save_img', action='store_true')

    F = args.parse_args()

    log = Logger('log.txt')

    if F.no_log:
        log.disabled = True

    if F.use_phone:
        from config import conf1 as conf  # 手机配置
        subprocess.call('adb devices', shell=True)
    else:
        from config import conf2 as conf
        subprocess.call('adb connect 127.0.0.1:62001', shell=True)
        subprocess.call('adb devices', shell=True)

    browser = webdriver.Chrome(chromedriver_path)
    browser.get('https://www.sogou.com/')
    # elem = browser.find_element_by_id('query')
    # elem.send_keys('问')
    # elem.send_keys(Keys.RETURN)

    if F.use_wx:
        # 初始化机器人，扫码登陆
        bot = Bot()
        # my_friend = bot.friends().search('姐')[0]
        group = bot.groups().search('答题')[0]
        print(group)

    # 创建管理器
    hm = pyHook.HookManager()
    # 监听键盘
    hm.KeyDown = onKeyboardEvent   
    hm.HookKeyboard()  
    # 循环监听
    pythoncom.PumpMessages()