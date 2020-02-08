# coding:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_mainwindow import Ui_MainWindow
from Screenshot import Screenshot
from ROI import ROI
import sys
from utils import *
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import cv2
import jieba
import jieba.posseg as pseg
import os
from collections import Counter, OrderedDict
import traceback


hl_excluded_words = stop_words|set(['.','=',';','"',':','<','>','-'])

class Worker(QThread):
    """docstring for Worker"""
    finished = pyqtSignal()
    def __init__(self, target, *args, **kw):
        super(Worker, self).__init__()
        self.target = target
        self.args = args
        self.kw = kw
        self.res = None

    def run(self):
        self.res = self.target(*self.args, **self.kw)
        self.finished.emit()


class PlanA1(QThread):
    """docstring for PlanA1"""
    finished = pyqtSignal()
    showQue = pyqtSignal(str)
    showRes = pyqtSignal(str,int)
    showScore = pyqtSignal(dict, bool)
    def __init__(self, parent):
        super(PlanA1, self).__init__()
        self._p = parent
        self.que = None
        self.opt_list = None

    def run(self):
        """直接题： 直接检索问题"""

        uid = rand_name()
        self._p.uid = uid
        try:
            que = self.que
            opt_list = self.opt_list
            opts = ' '.join(opt_list)
            que = adjust_search_que(que)
            self._p.logger.info('{} 题目 {}'.format(uid, que+' '+opts))
            self.showQue.emit(que+' '+opts)

            text = self._p.baidus[-1].search_and_extract_page(que)
            score = baidu_score(text, opt_list, que, cut='later_cut') 

            if sum(score.values())==0:
                text = self._p.baidus[-1].search_and_extract_page(que+' '+opts)
                score = baidu_score(text, opt_list, que, cut='later_cut')

                html = re.sub(r'\n', '<br>', text)
                pat = r"({})".format('|'.join(opt_list))
                html = re.sub(pat, r'<span style="color:red;">\1</span>', html, flags=re.I)
                html = '<div style="font-size: 16px;">{}</div>'.format(html)
            else:
                html = re.sub(r'\n', '<br>', text)
                pat = r"({})".format('|'.join(opt_list))
                html = re.sub(pat, r'<span style="color:red;">\1</span>', html, flags=re.I)
                html = '<div style="font-size: 16px;">{}</div>'.format(html)

            self.showRes.emit(html,1)
            self.showScore.emit(score, False)

        except Exception as e:
            print(e)
            self._p.logger.info("{} {}".format(uid, e))

        if not self._p.debug and self._p.save_img:
            try:
                cv2.imwrite('debug_images/{}.png'.format(uid), self._p.img)
            except Exception as e:
                print(e)
                self._p.logger.info("{}".format(e))

        self.finished.emit()


class PlanA2(QThread):
    """docstring for PlanA1"""
    finished = pyqtSignal()
    showRes = pyqtSignal(str,int)
    def __init__(self, parent):
        super(PlanA2, self).__init__()
        self._p = parent
        self.que = None
        self.opt_list = None

    def run(self):
        uid = rand_name()
        self._p.uid = uid
        try:
            que = self.que
            opt_list = self.opt_list
            opts = ' '.join(opt_list)
            que = adjust_search_que(que)

            workers = []
            for i, opt in enumerate(opt_list):
                w = Worker(self._p.baidus[i].search_and_extract_item, que+' '+opt, opt)
                w.start()
                workers.append(w)

            html = []
            for i, opt in enumerate(opt_list):
                workers[i].wait()
                words = jieba.cut(opt)
                pat = "|".join([w for w in words if w not in hl_excluded_words])
                pat = r"({})".format(pat)
                item = re.sub(pat, r'<span style="color:red;">\1</span>', re.sub(r'\n', '<br>', workers[i].res), flags=re.I)
                html.append(">>>>{}<br>{}".format(opt, item))
            
            html = '<hr>'.join(html)
            pat = "|".join([w for w in jieba.cut(que) if w not in hl_excluded_words])
            pat = r"({})".format(pat)
            html = re.sub(pat, r'<span style="color:blue;">\1</span>', html, flags=re.I)
            html = '<div style="font-size: 16px;">{}</div>'.format(html)
            # print(html)
            self.showRes.emit(html,2)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self._p.logger.info("{} {}".format(uid, e))

        self.finished.emit()


class BaiduSearch(QObject):

    def __init__(self, driver_path, headless=False):
        super().__init__()
        self._browser = baidu_browser_init(driver_path, headless)

    def quit(self):
        self._browser.quit()

    def search_and_extract_page(self, kw):
        self._search(kw)
        try:
            self._wait()
        except:
            return 'timeout!'
        return self._extract_page_text()

    def search_and_extract_item(self, kw, opt):
        self._search(kw)
        try:
            self._wait()
        except:
            return 'timeout!'
        return self._extract_item_text(opt)

    def search_and_extract_time(self, kw):
        self._search(kw+'哪一年诞生发生')
        try:
            self._wait()
        except:
            return 'timeout!'
        return self._extract_time()

    def _search(self, kw):
        if len(self._browser.find_elements_by_css_selector('div#content_left')) > 0:
            self._browser.back()
            # time.sleep(.2)
        baidu_search(self._browser, kw)

    @run_time
    def _wait(self, pic=False):
        if pic:
            WebDriverWait(self._browser,4,0.01).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.card-page")))
        else:
            WebDriverWait(self._browser,2.5,0.01).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.c-container")))
        # time.sleep(.2)

    def _extract_page_text(self):
        res_list = self._browser.find_elements_by_css_selector('div.c-container')
        text = []
        for r in res_list:
            try:
                title = r.find_element_by_css_selector('h3.t').text 
            except:
                try:
                    title = r.find_element_by_css_selector('h3.c-title').text
                except:
                    title = ''
            try:
                abst = r.find_element_by_css_selector('div.c-abstract').text
            except:
                try:
                    abst = r.find_element_by_css_selector('div.c-span-last').text
                except:
                    continue
            text.append(title)
            text.append(abst)
        text = re.sub(r"(更多关于.*?的问题>>)|(\d+年\d+月\d+日\s+-\s+)", '', '\n'.join(text))
        return text

    def _extract_item_text(self, kw):
        try:
            res_list = self._browser.find_elements_by_css_selector('div.c-container')
            text = ''
            for r in res_list:
                try:
                    title = r.find_element_by_css_selector('h3.t').text 
                except:
                    try:
                        title = r.find_element_by_css_selector('h3.c-title').text
                    except:
                        title = ''
                try:
                    abst = r.find_element_by_css_selector('div.c-abstract').text
                except:
                    try:
                        abst = r.find_element_by_css_selector('div.c-span-last').text
                    except:
                        continue
                text = re.sub(r'(\d+年\d+月\d+日\s+-\s+)|(更多关于.*?的问题>>)', '', title + '\n' + abst)
                if isRelated(kw, text):
                    break
        except:
            text = 'error!'
            print(traceback.format_exc())
        return text

    def search_pic_and_extract_text(self, file):
        text = ''
        try:
            self._browser.find_element_by_class_name('soutu-btn').click()
            input = self._browser.find_element_by_css_selector('input.upload-pic')
            input.send_keys(file)
            self._wait(pic=True)
            text = self._browser.find_element_by_css_selector('div.card-page').text
        except Exception as e:
            print(e)
            
        self._browser.back()
        return text

    def _extract_time(self):
        text = self._extract_page_text()
        year_list = re.findall(r"(\d+)\s*年", text)
        try:
            year, _ = Counter(year_list).most_common(1)[0]
        except:
            year = ''
        return year


class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow"""
    showQue = pyqtSignal(str)
    showScore = pyqtSignal(dict, bool)
    showRes = pyqtSignal(str, int)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.r = ROI()
        self.s = None
        self.logger = Logger('log.txt')
        self.logger.disabled = False
        self.save_img = True
        self.uid = None
        self.debug = False
        self.roi_geometry = None
        chromedriver_path = 'chromedriver/chromedriver.exe'
        if not os.path.exists('debug_images'):
            os.mkdir('debug_images')

        self.baidus = []
        workers = []
        for i in range(5):
            w = Worker(BaiduSearch, chromedriver_path, headless=True)  # if i<4 else False
            w.start()
            workers.append(w)
        for w in workers:
            w.wait()
            self.baidus.append(w.res)

        self.showQue.connect(self.onShowQue)
        self.showRes.connect(self.onShowRes)
        self.showScore.connect(self.onShowScore)

        self.picWorker = None

        self.planA1 = PlanA1(parent=self)
        self.planA2 = PlanA2(parent=self)
        self.t1 = None
        self.t2 = None

        self.planA1.showQue.connect(self.onShowQue)
        self.planA1.showRes.connect(self.onShowRes)
        self.planA1.showScore.connect(self.onShowScore)
        self.planA2.showRes.connect(self.onShowRes)
        self.planA1.finished.connect(self.handlePlanA1Finished)
        self.planA2.finished.connect(self.handlePlanA2Finished)


    def handlePlanA1Finished(self):
        print("---- {} elapsed: {:.3f}s".format('planA1', time.time()-self.t1))

    def handlePlanA2Finished(self):
        print("---- {} elapsed: {:.3f}s".format('planA2', time.time()-self.t2))

    def keyPressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            self.simple(ocr=False)
        elif event.key() == Qt.Key_F1:
            self.simple()
        elif event.key() == Qt.Key_F2:
            self.planA()
        elif event.key() == Qt.Key_F3:
            self.planB()
        elif event.key() == Qt.Key_F4:
            self.planC()
        elif event.key() == Qt.Key_F7:
            self.on_pushButton_pic_clicked()

    @pyqtSlot()
    def on_pushButton_search_clicked(self):
        self.simple(ocr=False)

    @pyqtSlot()
    def on_pushButton_simple_clicked(self):
        self.simple()

    @pyqtSlot()
    def on_pushButton_planA_clicked(self):
        self.planA()

    @pyqtSlot()
    def on_pushButton_planB_clicked(self):
        self.planB()

    @pyqtSlot()
    def on_pushButton_planC_clicked(self):
        self.planC()

    @pyqtSlot()
    def on_pushButton_pic_clicked(self):
        self.s = Screenshot()
        self.s.captured.connect(self.handleCaptured)
        self.s.closed.connect(self.handleScreenshotClosed)
        self.roi_geometry = self.r.geometry()
        self.r.hide()
        self.s.show()

    def handleCaptured(self, pixmap):
        uid = rand_name()
        file = os.path.join(os.path.abspath('.'), 'debug_images', uid+'.png')
        pixmap.save(file, 'PNG', 5)
        self.picWorker = Worker(self.baidus[-1].search_pic_and_extract_text, file)
        self.picWorker.finished.connect(self.handlePicWorkerFinished)
        self.picWorker.start()

    def handlePicWorkerFinished(self):
        res = self.picWorker.res
        html = '<div style="font-size:16px;">>>>>图片题<br>{}</div>'.format(re.sub(r'\n', '<br>', res))
        self.onShowRes(html,1)

    def handleScreenshotClosed(self):
        self.r.setGeometry(self.roi_geometry)
        self.r.show()

    def onShowQue(self, que):
        self.plainTextEdit_que.setPlainText(que)

    def onShowRes(self, html, flag):
        if flag == 1:
            self.textBrowser_res.moveCursor(QTextCursor.Start)
            self.textBrowser_res.insertHtml(html)
            self.textBrowser_res.insertHtml("<br><br>{}<br><br>".format('='*60))
        else:
            self.textBrowser_res_2.moveCursor(QTextCursor.Start)
            self.textBrowser_res_2.insertHtml(html)
            self.textBrowser_res_2.insertHtml("<br><br>{}<br><br>".format('='*60))

    def onShowScore(self, score, append):
        try:
            ans, ans_bak = max(score, key=score.get), min(score, key=score.get)
        except:
            ans = ans_bak = '--'
        if append:
            self.textBrowser_score.moveCursor(QTextCursor.End)
            self.textBrowser_score.insertHtml('<div style="font-size:16px;">{}<br><br>(B) 推荐答案: {}{}备选: {}<div>'.format(score,ans, '&nbsp;'*8, ans_bak))
        else:
            self.textBrowser_score.setHtml('<div style="font-size: 16px;">{}<br><br>(A) 推荐答案: {}{}备选: {}</div>'.format(score, ans, '&nbsp;'*8, ans_bak))
            self.textBrowser_score.moveCursor(QTextCursor.End)
            self.textBrowser_score.insertHtml("<br><br>{}<br><br>".format('='*60))
            
        self.logger.info('{} 百度打分 {}'.format(self.uid, score))

    @pyqtSlot()
    def on_pushButton_roi_clicked(self):
        self.r.show()

    # @pyqtSlot()
    def on_checkBox_logging_stateChanged(self, s):
        if s == 0:
            self.logger.disabled = True
        else:
            self.logger.disabled = False

    # @pyqtSlot()
    def on_checkBox_saveImg_stateChanged(self, s):
        if s == 0:
            self.save_img = False
        else:
            self.save_img = True

    # @pyqtSlot()
    def on_checkBox_debug_stateChanged(self, s):
        if s == 0:
            self.debug = False
        else:
            self.debug = True

    @run_time
    def simple(self, ocr=True):
        uid = rand_name()
        self.uid = uid
        try:
            if ocr:
                if self.debug:
                    text_list = [
                        # '以下选项中,第一批被列入国家级非物质文化遗产的是? 凉茶 珠算 酥油茶',
                        # "化学分子构型理论,种物质是四面体? 白磷 磷化氢 乙炔 三氟化硼",
                        # '关于沈从文的小说《边城》,下列说法不正确的是哪项? 以小镇茶峒为背景 描绘了湘西风土人情 荣获茅盾文学奖',
                        '下列黄果树瀑布说法不正确是?',
                        '有关“草履虫"的描述不正确的是哪项?',
                        '清朝皇帝年号庙号对应?',
                        '国宝级文物诞生西周时期?',
                        # "澳门回归时唱响的《七子之歌》的词作者是 哪个诗歌流派的? 朦胧派 新月派 湖畔派",
                        # '以下哪个项目不属于今年举行的世界军人运动 会上的项目? 跳伞 击剑 散打',
                        # '小明乘坐高铁时发现车辆正疾驰穿过航站 楼,请问他正在哪一机场附近? 北京大兴国际机场 厦门高崎国际机场 广州白云国际机场',
                        # '中国女排目前已经十度成为世界冠军,其中包 含了奥运会、世界杯和哪项赛事? 国际排联大冠军杯 世俱杯 世锦赛',
                        # '以下哪项措施可能帮助宝宝远离红屁屁? 换上帮宝适泡泡纸尿裤 给宝宝唱首歌 多喝热水',
                        # '李健作词作曲并唱道“那里春风沉醉,那里绿草如茵”说的是哪个地方? 江南水乡 呼伦贝尔大草原 贝加尔湖畔',
                        # '动画片《葫芦娃》中,五娃的技能是? 隐身 吐火 吐水',
                        # '小提琴有4根弦,那么大提琴有几根弦? 4 5 6',
                        # '小说《天龙八部》中,虛竹的配偶梦姑是哪国的公主? 西夏 大理 吐蕃',
                        # '近年来备受热捧的“脏脏包"是哪一类网红商 品? 食物 箱包 洁具',
                        '00后网络聊天时经常使用的缩写“XSWL"是在表达哪种情绪?',
                        # '80年代风靡全国的“燕舞,燕舞,一曲歌来片情″是哪种商品的广告歌曲? 收录机 电视机 卡拉OK机'
                        ]
                    que = np.random.choice(text_list)
                else:
                    img = self.screenshot()
                    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    _, buf = cv2.imencode(".png", gray)
                    ocr_res = ocr2(bytes(buf))
                    que = del_num(''.join([t['words'] for t in ocr_res]))
                self.logger.info('{} 题目 {}'.format(uid, que))
                que = adjust_search_que(que)
                self.showQue.emit(que)     
            else:
                que = self.plainTextEdit_que.toPlainText()
            text = self.baidus[-1].search_and_extract_page(que)
            words = [w for w in jieba.cut(que) if w not in hl_excluded_words]
            pat = r"({})".format('|'.join(words))
            html = re.sub(pat, r'<span style="color:blue;">\1</span>', re.sub(r'\n','<br>',text), flags=re.I)
            html = '<div style="font-size: 16px;">{}</div>'.format(html)
            self.showRes.emit(html,1)
        except Exception as e:
            print(e)
            self.logger.info("{} {}".format(uid, e))
            print(traceback.format_exc())

        if ocr and not self.debug and self.save_img:
            try:
                cv2.imwrite('debug_images/{}.png'.format(uid), img)
            except Exception as e:
                print(e)
                self.logger.info("{}".format(e))

    # @run_time
    def planA(self):
        """直接题： 直接检索问题"""
        if self.debug:
            text_list = [
                # '以下选项中,第一批被列入国家级非物质文化遗产的是? 凉茶 珠算 酥油茶',
                # "化学分子构型理论,种物质是四面体? 白磷 磷化氢 乙炔 三氟化硼",
                # '关于沈从文的小说《边城》,下列说法不正确的是哪项? 以小镇茶峒为背景 描绘了湘西风土人情 荣获茅盾文学奖',
                '下列黄果树瀑布说法不正确是? 古称白水河瀑布 喀斯特地貌瀑布 中国最宽的瀑布',
                '有关“草履虫"的描述不正确的是哪项? 由一个细胞构成 雌雄同体 只有一种生殖方式',
                '清朝皇帝年号庙号对应? 乾隆一清高宗 道光-清文宗 光绪-清德宗 嘉庆-清仁宗',
                '国宝级文物诞生西周时期? 铸客大鼎 太保鼎 大盂鼎 利簋',
                # "澳门回归时唱响的《七子之歌》的词作者是 哪个诗歌流派的? 朦胧派 新月派 湖畔派",
                # '以下哪个项目不属于今年举行的世界军人运动 会上的项目? 跳伞 击剑 散打',
                # '小明乘坐高铁时发现车辆正疾驰穿过航站 楼,请问他正在哪一机场附近? 北京大兴国际机场 厦门高崎国际机场 广州白云国际机场',
                # '中国女排目前已经十度成为世界冠军,其中包 含了奥运会、世界杯和哪项赛事? 国际排联大冠军杯 世俱杯 世锦赛',
                # '以下哪项措施可能帮助宝宝远离红屁屁? 换上帮宝适泡泡纸尿裤 给宝宝唱首歌 多喝热水',
                # '李健作词作曲并唱道“那里春风沉醉,那里绿草如茵”说的是哪个地方? 江南水乡 呼伦贝尔大草原 贝加尔湖畔',
                # '动画片《葫芦娃》中,五娃的技能是? 隐身 吐火 吐水',
                # '小提琴有4根弦,那么大提琴有几根弦? 4 5 6',
                # '小说《天龙八部》中,虛竹的配偶梦姑是哪国的公主? 西夏 大理 吐蕃',
                # '近年来备受热捧的“脏脏包"是哪一类网红商 品? 食物 箱包 洁具',
                '00后网络聊天时经常使用的缩写“XSWL"是在 表达哪种情绪? 高兴 生气 悲伤',
                # '80年代风靡全国的“燕舞,燕舞,一曲歌来片情″是哪种商品的广告歌曲? 收录机 电视机 卡拉OK机'
                ]
            text = np.random.choice(text_list)
            que, opts = text.split('?')
            opt_list = opts.strip().split(' ')
        else:
            img = self.screenshot()
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            _, buf = cv2.imencode(".png", gray)
            ocr_res = ocr2(bytes(buf))
            que, opt_list = process_res(ocr_res)
            opts = ' '.join(opt_list)
            self.img = img

        self.planA1.que = que
        self.planA1.opt_list = opt_list
        self.planA2.que = que
        self.planA2.opt_list = opt_list
        self.planA1.start()
        self.t1 = time.time()
        self.planA2.start()
        self.t2 = time.time()

    @run_time
    def planB(self):
        """拐弯题"""

        uid = rand_name()
        self.uid = uid

        try:
            if self.debug:
                text_list = [
                            '被李白称赞道"墨池飞出北溟鱼,笔锋杀尽中山兔"的书法家创作了下列哪个作品? 孟法师碑 苦笋帖 皇甫诞碑 初月帖',
                            '曾担任清华教授,被誉为“公子的公子,教授之教授”的学者也著有以下哪部作品? 国音新诗韵 观堂集林 自由之路 寒柳堂集',
                            '曾自述“十五好剑术,遍干诸侯”的历史人物与下列哪位处于同朝代? 秦观 元稹 卫青 孙武',
                            ]
                text = np.random.choice(text_list)
                que, opts = text.split('?')
                opt_list = opts.strip().split(' ')
            else:
                img = self.screenshot()
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                _, buf = cv2.imencode(".png", gray)
                ocr_res = ocr2(bytes(buf))
                que, opt_list = process_res(ocr_res)
                opts = ' '.join(opt_list)

            self.logger.info('{} 题目 {}'.format(uid, que+' '+opts))
            que = adjust_search_que(que)
            self.showQue.emit(que+' '+opts)

            workers = []
            w = Worker(self.baidus[-1].search_and_extract_page, que)
            w.start()
            workers.append(w)
            for i, opt in enumerate(opt_list):
                w = Worker(self.baidus[i].search_and_extract_page, opt)
                w.start()
                workers.append(w)
            res = []
            for w in workers:
                w.wait()
                res.append(w.res)

            score = baidu_score(res[0], opt_list, que, cut='later_cut')          

            if sum(score.values())==0:
                text = self.baidus[-1].search_and_extract_page(que+' '+opts)
                score = baidu_score(text, opt_list, que, cut='later_cut')

                html = re.sub(r'\n', '<br>', text)
                pat = r"({})".format('|'.join(opt_list))
                html = re.sub(pat, r'<span style="color:red;">\1</span>', html, flags=re.I)
                html = '<div style="font-size: 16px;">{}</div>'.format(html)
            else:
                html = re.sub(r'\n', '<br>', res[0])
                pat = r"({})".format('|'.join(opt_list))
                html = re.sub(pat, r'<span style="color:red;">\1</span>', html, flags=re.I)
                html = '<div style="font-size: 16px;">{}</div>'.format(html)

            self.showRes.emit(html,1)
            self.showScore.emit(score, False)

            score2 = dict(zip(opt_list, corr_score(res)))
            self.showScore.emit(score2, True)

        except Exception as e:
            print(e)
            self.logger.info("{} {}".format(uid, e))
            print(traceback.format_exc())

        if not self.debug and self.save_img:
            try:
                cv2.imwrite('debug_images/{}.png'.format(uid), img)
            except Exception as e:
                print(e)
                self.logger.info("{}".format(e))

    @run_time
    def planC(self):
        """时间题: 检索选项出现的时间"""

        uid = rand_name()
        self.uid = uid

        try:
            if self.debug:
                text_list = [
                    '如果时光倒回到1648年,哪个历史事件还没有发生? 牛顿提出万有引力定律 麦哲伦开始环球航行 顺治皇帝已经即位 克伦威尔建立新军',
                    "迪斯尼那个出现的时间最晚? 唐老鸭 飞天狗 米老鼠",
                    '以下足球俱乐部中,哪一支的成立时间晚于1920年? 托特纳姆热刺 巴黎圣日耳曼 多特蒙德',
                    ]
                text = np.random.choice(text_list)
                que, opts = text.split('?')
                opt_list = opts.strip().split(' ')
            else:           
                img = self.screenshot()
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                _, buf = cv2.imencode(".png", gray)
                ocr_res = ocr2(bytes(buf))
                que, opt_list = process_res(ocr_res)
                opts = ' '.join(opt_list)
            
            self.logger.info('{} 题目 {}'.format(uid, que+' '+opts))
            self.showQue.emit(que+' '+opts)
            
            workers = []
            for i, opt in enumerate(opt_list):
                w = Worker(self.baidus[i].search_and_extract_time, opt)
                w.start()
                workers.append(w)
            years = []
            for i, opt in enumerate(opt_list):
                workers[i].wait()
                years.append(workers[i].res)
            time_dict = OrderedDict(sorted(dict(zip(years,opt_list)).items()))
            html = '<div style="font-size: 16px;">>>>>时间题<br>{}</div>'.format("<br>".join(["{}: {}".format(k,v) for k,v in time_dict.items()]))
            self.showRes.emit(html,1)
        except Exception as e:
            print(e)
            self.logger.info("{} {}".format(uid, e))

        if not self.debug and self.save_img:
            try:
                cv2.imwrite('debug_images/{}.png'.format(uid), img)
            except Exception as e:
                print(e)
                self.logger.info("{}".format(e))

    def screenshot(self):
        return self.r.screenshot()

    def closeEvent(self, event):
        super().closeEvent(event)
        workers = []
        for baidu in self.baidus:
            w = Worker(baidu.quit)
            w.start()
            workers.append(w)
        for w in workers:
            w.wait()
        QApplication.closeAllWindows()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
