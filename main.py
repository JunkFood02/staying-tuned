# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
from urllib import request

import threading
import time

import re

from bs4 import BeautifulSoup

Count = 0


def check_info():
    myURL = "http://jwc.hust.edu.cn/tzgg.htm"
    rep = request.urlopen(myURL).read()
    data = rep.decode('utf-8')
    soup = BeautifulSoup(data, "html.parser")
    for tag in soup.find_all(text=re.compile("转专业")):
        print(tag.text)
        os.system('osascript -e \'display notification "转专业通知已出" with title "转专业通知已出"\'')
        os.system('say "转专业通知已出"')
        exit()
    global Count
    Count += 1
    print("check for " + Count.__str__() + " times: NO INFO!")
    timer = threading.Timer(10, check_info)
    timer.start()


if __name__ == '__main__':
    check_info()
