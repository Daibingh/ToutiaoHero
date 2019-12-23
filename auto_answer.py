# coding:utf-8

import subprocess
import time
import cv2
import numpy as np
from utils import run_time, ocr, ocr2, Logger, toutiao_score
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
from datetime import datetime


search_engine = 'http://www.baidu.com'
chromedriver_path = './chromedriver_win32/chromedriver.exe'

# @run_time
def screencap():
    cmd = conf.cmd
    ret = subprocess.call(cmd, shell=True, timeout=3)
    return ret

@run_time
def crop_img(img_file):
    img = cv2.imread(img_file)
    x, y, w, h = conf.roi
    img = img[y:y+h,x:x+w]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 161, 255, cv2.THRESH_BINARY)
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 12)
    _, buf = cv2.imencode(".png", binary)
    return bytes(buf)

# @run_time
def process_res(res):
    text = ' '.join([t.get('words').strip() for t in res])
    # que_opt = text[2:].split('?')
    # que_opt[0] += '?'
    ind = text.find('.')
    return text[ind+1:]


def move_image(dist_folder, uid):
    shutil.move(conf.img_folder+'screen.png', dist_folder+uid+'.png')  # 移动文件

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
    print(chr(27) + "[2J")  # clear terminal

    uid = uuid.uuid4().hex
    # ret = screencap()
    if ret != 0:
        print('\033[1;31m---- adb offline!\033[0m')
        return
    try:
        img_bytes = crop_img(conf.img_folder+'screen.png')
        ocr_res = ocr2(img_bytes)
        search_text = process_res(ocr_res)
        que, opts = search_text.split('?')
        search_text = que.replace(' ', '') + '?' + opts
        print(">>>> 搜索的关键词是: {}".format(search_text))
        log.info("{}: 搜索关键词 {}".format(uid, search_text))

        elem = browser.find_element_by_id("kw")
        elem.clear()
        elem.send_keys(search_text)
        elem.send_keys(Keys.RETURN)

        if F.use_toutiao:
            opt_score2 = toutiao_score(search_text)
            if sum(opt_score2.values()) == 0:
                toutiao_ans, toutiao_ans_bak = '--', '--'
            else:
                toutiao_ans, toutiao_ans_bak = max(opt_score2, key=opt_score2.get), min(opt_score2, key=opt_score2.get)
        else:
            time.sleep(F.wait_time)
        WebDriverWait(browser,2,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.result.c-container")))

        opt_score = baidu_score(browser, opts.strip().split(' '))
        if sum(opt_score.values()) == 0:
            baidu_ans, baidu_ans_bak = '--', '--'
        else:
            baidu_ans, baidu_ans_bak = max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)

        print('>>>> 百度打分: {}'.format(opt_score))
        log.info("{}: 百度打分 {}".format(uid, opt_score))
        if F.use_toutiao:
            print('>>>> 头条打分: {}'.format(opt_score2))
            log.info("{}: 头条打分 {}".format(uid, opt_score2))
        print('\n')
        print(">>>> 百度推荐答案: {}, 备选(否定题目): {}".format(baidu_ans, baidu_ans_bak))
        if F.use_toutiao:
            print(">>>> 头条推荐答案: {}, 备选(否定题目): {}".format(toutiao_ans, toutiao_ans_bak))
        print('------------------------------------------------------')

        if F.use_wx:
            msg = "百度: {}, 备选: {}".format(baidu_ans, baidu_ans_bak)
            if F.use_toutiao:
                msg = "头条: {}, 备选: {}\n".format(toutiao_ans, toutiao_ans_bak) + msg
            group.send(msg)

    except Exception as e:
        print('----', e)
        print(traceback.format_exc())
        log.info('{}: {}'.format(uid, e))
        if F.use_wx: group.send("error!")
    try:
        if not F.no_save_img:
            move_image('debug_images/', uid)
    except Exception as e:
        print('----', e)
        print(traceback.format_exc())


@run_time
def test():
    # print(chr(27) + "[2J")

    search_text_list = ['以下选项中,第一批被列入国家级非物质文化遗产的是? 凉茶 珠算 酥油茶',
                    # "进博会吉祥物叫什么名字? 招财 进宝 来福",
                    # "澳门回归时唱响的《七子之歌》的词作者是 哪个诗歌流派的? 朦胧派 新月派 湖畔派",
                    # '小明来到北京大兴国际机场的餐厅用餐时,发现? 价高质低 同质同价 同质价高',
                    # '以下哪个项目不属于今年举行的世界军人运动 会上的项目? 跳伞 击剑 散打',
                    # '小明乘坐高铁时发现车辆正疾驰穿过航站 楼,请问他正在哪一机场附近? 北京大兴国际机场 厦门高崎国际机场 广州白云国际机场',
                    # '中国女排目前已经十度成为世界冠军,其中包 含了奥运会、世界杯和哪项赛事? 国际排联大冠军杯 世俱杯 世锦赛',
                    '乐队“盘尼西林”的名字是哪种药物的音译名? 青霉素 黄曲霉素 红霉素',
                    # '动画片《葫芦娃》中,五娃的技能是? 隐身 吐火 吐水',
                    # '小提琴有4根弦,那么大提琴有几根弦? 4 5 6',
                    # '小说《天龙八部》中,虛竹的配偶梦姑是哪国的公主? 西夏 大理 吐蕃',
                    # '近年来备受热捧的“脏脏包"是哪一类网红商 品? 食物 箱包 洁具',
                    # '00后网络聊天时经常使用的缩写“XSWL"是在 表达哪种情绪? 高兴 生气 悲伤',
                    # '80年代风靡全国的“燕舞,燕舞,一曲歌来 片情″是哪种商品的广告歌曲? 收录机 电视机 卡拉OK机'
                    ]
    search_text = np.random.choice(search_text_list)
    que, opts = search_text.split('?')
    search_text = que.replace(' ', '') + '?' + opts
    print(">>>> 搜索的关键词是: {}".format(search_text))

    elem = browser.find_element_by_id("kw")
    elem.clear()
    elem.send_keys(search_text)
    elem.send_keys(Keys.RETURN)

    if F.use_toutiao:
        opt_score2 = toutiao_score(search_text)
        if sum(opt_score2.values()) == 0:
            toutiao_ans, toutiao_ans_bak = '--', '--'
        else:
            toutiao_ans, toutiao_ans_bak = max(opt_score2, key=opt_score2.get), min(opt_score2, key=opt_score2.get)
    else:
        time.sleep(F.wait_time)

    WebDriverWait(browser,2,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.result.c-container")))

    opt_score = baidu_score(browser, opts.strip().split(' '))
    if sum(opt_score.values()) == 0:
        baidu_ans, baidu_ans_bak = '--', '--'
    else:
        baidu_ans, baidu_ans_bak = max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)

    print('>>>> 百度打分: {}'.format(opt_score))
    if F.use_toutiao:
        print('>>>> 头条打分: {}'.format(opt_score2))
    print('\n')
    print(">>>> 百度推荐答案: {}, 备选(否定题目): {}".format(baidu_ans, baidu_ans_bak))
    if F.use_toutiao:
        print(">>>> 头条推荐答案: {}, 备选(否定题目): {}".format(toutiao_ans, toutiao_ans_bak))
    print('------------------------------------------------------')

    if F.use_wx:
        msg = "百度: {}, 备选: {}".format(baidu_ans, baidu_ans_bak)
        if F.use_toutiao:
            msg = "头条: {}, 备选: {}\n".format(toutiao_ans, toutiao_ans_bak) + msg
        group.send(msg)


def quit():
    browser.quit()
    sys.exit()

# @run_time
def check_state(img_file):
    delta = 3
    x,y,w,h = 48,325,625,24
    img = cv2.imread(img_file)
    roi = img[y:y+h,x:x+w]
    if roi.mean() < 255 - delta: return False
    x,y,w,h = conf.roi
    img = img[y:y+h,x:x+w]
    b, g, r = img[:,:,0],img[:,:,1],img[:,:,2]
    if np.logical_and(b > 231-delta, r < 43+delta).any(): return False
    if np.logical_and(r > 250-delta, g<92+delta).any(): return False
    return True

def get_time():
    now = datetime.now()
    return str(now).split(' ')[-1][:5]

def isOver(t):
    return t==get_time()

if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--use_phone', action='store_true')
    args.add_argument('--debug', action='store_true')
    args.add_argument('--use_wx', action='store_true')
    args.add_argument('--wait_time', type=float, default=.8)
    args.add_argument('--no_log', action='store_true')
    args.add_argument('--no_save_img', action='store_true')
    args.add_argument('--use_toutiao', action='store_true')
    args.add_argument('--sleep_time', type=int, default=50)
    args.add_argument('--deadline')

    F = args.parse_args()

    log = Logger('log.txt')

    if F.no_log:
        log.disabled = True

    if F.use_phone:
        from config import conf1 as conf  # 手机配置
        subprocess.call('adb devices', shell=True)
    else:
        from config import conf2 as conf
        subprocess.call('adb connect 127.0.0.1:62025', shell=True)
        subprocess.call('adb devices', shell=True)

    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    browser = webdriver.Chrome(chromedriver_path, options=option)
    browser.get(search_engine)

    if F.use_wx:
        # 初始化机器人，扫码登陆
        bot = Bot()
        # my_friend = bot.friends().search('姐')[0]
        group = bot.groups().search('答题')[0]
        print(group)


    time_interval = .11
    state_queue = []
    max_len = 3
    # sleep_time = 50
    # deadline = '21:30'

    try:
        while True:
            ret = screencap()
            curr_state = check_state(conf.img_folder+'screen.png')
            if len(state_queue) == max_len: state_queue.pop(0)
            state_queue.append(curr_state)

            if len(state_queue) == max_len and all(state_queue):
                if F.debug:
                    test()
                else:
                    main()
                time.sleep(F.sleep_time)

            if isOver(F.deadline): 
                quit()

            time.sleep(time_interval)
    except KeyboardInterrupt:
        quit()
