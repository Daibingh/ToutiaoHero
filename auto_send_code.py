import subprocess
import time
from datetime import datetime
import sys

# 980 1837
# 980 1032
def get_time():
    now = datetime.now()
    return str(now).split(' ')[-1][:5]

def run_cmd(cmd, t=1):
    ret = subprocess.call(cmd)
    time.sleep(t)
    return ret

def main():
    run_cmd('adb -s 35826afb0704 shell input tap 980 1837')
    run_cmd('adb -s 35826afb0704 shell input keyevent 279') 
    run_cmd('adb -s 35826afb0704 shell input tap 980 1032', t=10)
    return True


if __name__ == '__main__':
    
    run_cmd("adb devices")
    while get_time() != sys.argv[1]:
        main()