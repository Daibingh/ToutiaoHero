# coding:utf-8

class conf1(object):
    """手机配置"""
    roi = (72, 420, 938, 1020)  # (x,y,w,h)
    img_folder = './'
    cmd = 'adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png && adb shell rm /sdcard/screen.png'
    thresh = 100
        

class conf2(object):
    """夜神模拟器配置"""
    roi = (48, 200, 625, 550)  # ！
    roi_check = (48,325,625,24)
    img_folder = './'
    cmd = 'adb shell screencap -p /mnt/shared/Image/screen.png && adb pull /mnt/shared/Image/screen.png ./screen.png'
    port = 62025
    thresh = -1

class conf3(object):
    """逍遥模拟器配置"""
    roi = (34, 180, 653, 420)  # ！
    roi_check = (34,264,653,17)
    img_folder = './' 
    cmd = 'adb shell screencap -p /sdcard/Pictures/screen.png && adb pull /sdcard/Pictures/screen.png ./screen.png'
    port = 21503
    thresh = -1