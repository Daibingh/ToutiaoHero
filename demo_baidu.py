# coding:utf-8

import subprocess
import time
import cv2
import numpy as np
from utils import*
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PyHook3 as pyHook
import pythoncom
import sys
import uuid
from wxpy import *
import traceback
import argparse


hot_key = "F2"
chromedriver_path = './chromedriver_win32/chromedriver.exe'


@run_time
def main():
    print(chr(27) + "[2J")  # clear terminal

    uid = uuid.uuid4().hex
    img = screencap(F.device)
    try:
        img_bytes = crop_img(img, conf.roi)
        ocr_res = ocr2(img_bytes)
        # print(ocr_res)
        text = process_res(ocr_res)
        # print(search_text)
        que, opts = text.split('?')
        que = que.replace(' ', '') + '?'

        print(">>>> 搜索的关键词是: {}".format(que))
        log.info("{}: 搜索关键词 {}".format(uid, que))

        baidu_search(browser, que)

        time.sleep(F.wait_time)
        WebDriverWait(browser,3,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.result.c-container")))

        opt_score = baidu_score(browser, opts.strip().split(' '), que=que)

        if not isStable(que, opt_score):
            que = adjust_search_que(que, 38-get_text_width(opts))
            search_text = que + opts
            print(">>>> 搜索的关键词是: {}".format(search_text))
            log.info("{}: 搜索关键词 {}".format(uid, search_text))
            baidu_search(browser, search_text)
            time.sleep(F.wait_time)
            WebDriverWait(browser,3,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.result.c-container")))
            opts_list = opts.strip().split(' ')
            opt_score = baidu_score(browser, opts_list, que=que, cut='later_cut')

        if sum(opt_score.values()) == 0:
            baidu_ans, baidu_ans_bak = '--', '--'
        else:
            baidu_ans, baidu_ans_bak = max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)

        print('>>>> 百度打分: {}'.format(opt_score))
        log.info("{}: 百度打分 {}".format(uid, opt_score))
        print('\n')
        print(">>>> 百度推荐答案: {}, 备选(否定题目): {}".format(baidu_ans, baidu_ans_bak))
        print('------------------------------------------------------')

        if F.use_wx:
            msg = "百度: {}, 备选: {}".format(baidu_ans, baidu_ans_bak)
            group.send(msg)

    except Exception as e:
        print('----', e)
        print(traceback.format_exc())
        log.info('{}: {}'.format(uid, e))
        if F.use_wx: group.send("error!")

    if not F.no_save_img:
        cv2.imwrite('debug_images/{}.png'.format(uid), img)


@run_time
def test():
    print(chr(27) + "[2J")

    search_text_list = [
                    # '以下选项中,第一批被列入国家级非物质文化遗产的是? 凉茶 珠算 酥油茶',
                    # "进博会吉祥物叫什么名字? 招财 进宝 来福",
                    # '关于沈从文的小说《边城》,下列说法不正确的是哪项? 以小镇茶峒为背景 描绘了湘西风土人情 荣获茅盾文学奖',
                    '下列黄果树瀑布说法不正确是? 古称白水河瀑布 喀斯特地貌瀑布 中国最宽的瀑布',
                    # '有关“草履虫"的描述不正确的是哪项? 由一个细胞构成 雌雄同体 只有一种生殖方式',
                    # "澳门回归时唱响的《七子之歌》的词作者是 哪个诗歌流派的? 朦胧派 新月派 湖畔派",
                    # '小明来到北京大兴国际机场的餐厅用餐时,发现? 价高质低 同质同价 同质价高',
                    # '以下哪个项目不属于今年举行的世界军人运动 会上的项目? 跳伞 击剑 散打',
                    # '小明乘坐高铁时发现车辆正疾驰穿过航站 楼,请问他正在哪一机场附近? 北京大兴国际机场 厦门高崎国际机场 广州白云国际机场',
                    # '中国女排目前已经十度成为世界冠军,其中包 含了奥运会、世界杯和哪项赛事? 国际排联大冠军杯 世俱杯 世锦赛',
                    # '以下哪项措施可能帮助宝宝远离红屁屁? 换上帮宝适泡泡纸尿裤 给宝宝唱首歌 多喝热水',
                    # '李健作词作曲并唱道“那里春风沉醉,那里绿草如茵”说的是哪个地方? 江南水乡 呼伦贝尔大草原 贝加尔湖畔',
                    # '动画片《葫芦娃》中,五娃的技能是? 隐身 吐火 吐水',
                    # '小提琴有4根弦,那么大提琴有几根弦? 4 5 6',
                    # '小说《天龙八部》中,虛竹的配偶梦姑是哪国的公主? 西夏 大理 吐蕃',
                    # '近年来备受热捧的“脏脏包"是哪一类网红商 品? 食物 箱包 洁具',
                    # '00后网络聊天时经常使用的缩写“XSWL"是在 表达哪种情绪? 高兴 生气 悲伤',
                    # '80年代风靡全国的“燕舞,燕舞,一曲歌来 片情″是哪种商品的广告歌曲? 收录机 电视机 卡拉OK机'
                    ]
    text = np.random.choice(search_text_list)
    que, opts = text.split('?')
    que = que.replace(' ', '') + '?'

    print(">>>> 搜索的关键词是: {}".format(que))

    baidu_search(browser, que)
    
    time.sleep(F.wait_time)
    WebDriverWait(browser,3,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.result.c-container")))

    opt_score = baidu_score(browser, opts.strip().split(' '), que=que)

    if not isStable(que, opt_score):
        que = adjust_search_que(que, 38-get_text_width(opts))
        search_text = que + opts
        print(">>>> 搜索的关键词是: {}".format(search_text))
        baidu_search(browser, search_text)
        time.sleep(F.wait_time)
        WebDriverWait(browser,3,0.1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.result.c-container")))
        opts_list = opts.strip().split(' ')
        opt_score = baidu_score(browser, opts_list, que=que, cut='later_cut')

    if sum(opt_score.values()) == 0:
        baidu_ans, baidu_ans_bak = '--', '--'
    else:
        baidu_ans, baidu_ans_bak = max(opt_score, key=opt_score.get), min(opt_score, key=opt_score.get)

    print('>>>> 百度打分: {}'.format(opt_score))
    print('\n')
    print(">>>> 百度推荐答案: {}, 备选(否定题目): {}".format(baidu_ans, baidu_ans_bak))
    print('------------------------------------------------------')

    if F.use_wx:
        msg = "百度: {}, 备选: {}".format(baidu_ans, baidu_ans_bak)
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
    args.add_argument('--device', choices=['phone', 'yeshen', 'xiaoyao'])
    args.add_argument('--debug', action='store_true')
    args.add_argument('--use_wx', action='store_true')
    args.add_argument('--wait_time', type=float, default=.8)
    args.add_argument('--no_log', action='store_true')
    args.add_argument('--no_save_img', action='store_true')

    F = args.parse_args()

    log = Logger('log.txt')

    if F.no_log:
        log.disabled = True

    if F.device == 'phone':
        from config import conf1 as conf  # 手机配置
        subprocess.call('adb devices', shell=True)
    elif F.device == 'yeshen':
        from config import conf2 as conf
        subprocess.call('adb connect 127.0.0.1:{}'.format(conf.port), shell=True)
        subprocess.call('adb devices', shell=True)
    elif F.device == 'xiaoyao':
        from config import conf3 as conf
        subprocess.call('adb connect 127.0.0.1:{}'.format(conf.port), shell=True)
        subprocess.call('adb devices', shell=True)

    if F.use_wx:
        # 初始化机器人，扫码登陆
        bot = Bot()
        # my_friend = bot.friends().search('姐')[0]
        group = bot.groups().search('答题')[0]
        print(group)

    browser = baidu_browser_init(chromedriver_path)

    # 创建管理器
    hm = pyHook.HookManager()
    # 监听键盘
    hm.KeyDown = onKeyboardEvent   
    hm.HookKeyboard()  
    # 循环监听
    pythoncom.PumpMessages()
