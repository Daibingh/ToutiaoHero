# coding:utf-8

class conf1(object):
    """手机配置"""
    roi = (72, 380, 938, 940)  # (x,y,w,h)
    img_folder = './'
    cmd = 'adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png && adb shell rm /sdcard/screen.png'
        

class conf2(object):
    """夜神模拟器配置"""
    roi = (48, 200, 625, 550)  # ！
    roi_check = (48,325,625,24)
    img_folder = './'
    cmd = 'adb shell screencap -p /mnt/shared/Image/screen.png && adb pull /mnt/shared/Image/screen.png ./screen.png'
    port = 62025

class conf3(object):
    """逍遥模拟器配置"""
    roi = (34, 171, 653, 460)  # ！
    roi_check = (34,264,653,17)
    img_folder = './' 
    cmd = 'adb shell screencap -p /sdcard/Pictures/screen.png && adb pull /sdcard/Pictures/screen.png ./screen.png'
    port = 21503