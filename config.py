# coding:utf-8

class conf1(object):
    """手机配置"""
    roi = (72, 380, 938, 940)  # (x,y,w,h)
    img_folder = './'
    cmd = 'adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png && adb shell rm /sdcard/screen.png'
        

class conf2(object):
    """模拟器配置"""
    roi = (48, 245, 625, 650)  # ！
    img_folder = 'C:/Users/hdb/Nox_share/ImageShare/'
    cmd = 'adb shell screencap -p /mnt/shared/Image/screen.png'