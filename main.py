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
listurl = ["http://jwc.hust.edu.cn/",
           "http://sse.hust.edu.cn/tztg.htm",
           "http://fayixi.tjmu.edu.cn/rcpy1/bksjy/jxdt.htm",
           "http://stomatology.hust.edu.cn/xwzx/tzgg.htm",
           "http://cse.hust.edu.cn/index.htm",
           "http://www.cs.hust.edu.cn/",
           "http://mse.hust.edu.cn/sylm/tzgg.htm",
           "http://oei.hust.edu.cn/ywtz.htm",
           # "http://m.hust1st.com/col.jsp?id=130",
           "https://www.tjh.com.cn/channels/290.html",
           "http://humanity.hust.edu.cn/tzgg.htm",
           "http://eco.hust.edu.cn/index.htm",
           "http://seee.hust.edu.cn/xwzx/tzgg.htm",
           "http://ei.hust.edu.cn/bkjy/tzgg.htm",
           "http://sfl.hust.edu.cn/bkjx/jxtz.htm",
           "http://maths.hust.edu.cn/index/tzgg.htm",
           "http://aia.hust.edu.cn/bksjy/zxtz.htm",
           "http://phys.hust.edu.cn/rcpy/bksjy/tzgg.htm"
           ]
listschools = ["教务处",
               "软件学院",
               "法医学系",
               "口腔医学院",
               "网络安全学院",
               "计算机学院",
               "机械学院",
               "光电学院",
               # "第一临床学院",
               "第二临床学院",
               "人文学院",
               "经济学院",
               "电气学院",
               "电信学院",
               "外国语学院",
               "数学学院",
               "自动化学院",
               "物理学院"
               ]
listtexts = []


def check_info():
    for index in range(len(listurl)):
        flag = False
        myURL = listurl[index]
        rep = request.urlopen(myURL).read()
        data = rep.decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")
        for tag in soup.find_all(text=re.compile("转专业")):
            # if re.search("2021", tag.text, re.S):
            if tag.text not in listtexts:
                listtexts.append(tag.text)
                print(tag.text)
                flag = True
        if flag:
            print(listschools[index] + " 有新结果")
            os.system('osascript -e \'display notification "转专业消息有新结果" with title "请到程序窗口查看"\'')
            os.system('say "转专业消息有新结果"')
    global Count
    Count += 1
    print("check for " + Count.__str__() + " times")
    timer = threading.Timer(60, check_info)
    timer.start()


def get_info():
    for index in range(len(listurl)):
        myURL = listurl[index]
        rep = request.urlopen(myURL).read()
        data = rep.decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")
        for tag in soup.find_all(text=re.compile("转专业")):
            if tag.text not in listtexts:
                listtexts.append(tag.text)


if __name__ == '__main__':
    get_info()
    check_info()
