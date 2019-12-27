# coding:utf-8

class conf1(object):
    """手机配置"""
    roi = (72, 420, 938, 1020)  # (x,y,w,h)
    thresh = -1
    serial = "35826afb0704"


class conf2(object):
    """夜神模拟器配置"""
    roi = (48, 200, 625, 550)  # ！
    roi_check = (48,325,625,24)
    port = 62025
    thresh = -1


class conf3(object):
    """逍遥模拟器配置"""
    roi = (34, 180, 653, 420)  # ！
    roi_check = (34,264,653,17)
    port = 21503
    thresh = -1