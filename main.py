import os
import urllib.error
from urllib import request

import threading
import platform
import re
from notifypy import Notify
from bs4 import BeautifulSoup

Count = 0
listurl = ["http://jwc.hust.edu.cn/",
           "http://sse.hust.edu.cn/tztg.htm",
           "http://fayixi.tjmu.edu.cn/rcpy1/bksjy/jxdt.htm",
           "http://stomatology.hust.edu.cn/xwzx/gsl.htm",
           "http://cse.hust.edu.cn/index.htm",
           "http://www.cs.hust.edu.cn/",
           "http://mse.hust.edu.cn/sylm/tzgg.htm",
           "http://oei.hust.edu.cn/ywtz.htm",
           # "http://m.hust1st.com/col.jsp?id=130",
           "https://www.tjh.com.cn/channels/290.html",
           "http://humanity.hust.edu.cn/tzgg.htm",
           "http://eco.hust.edu.cn/index.htm",
           "http://seee.hust.edu.cn/xwzx/tzgg.htm",
           "http://ei.hust.edu.cn/index.htm",
           "http://sfl.hust.edu.cn/bkjx/jxtz.htm",
           "http://maths.hust.edu.cn/index/tzgg.htm",
           "http://aia.hust.edu.cn/tzgg/bks.htm",
           "http://phys.hust.edu.cn/rcpy/bksjy/tzgg.htm",
           "http://cm.hust.edu.cn/old/bk/jwgg.htm",
           "http://soci.hust.edu.cn/bksjy/tzgg.htm",
           "http://civil.hust.edu.cn/index/tzgg.htm",
           "http://cpa.hust.edu.cn/zsjx/bks/jwxx.htm",
           "http://life.hust.edu.cn/tzgg/bksjy.htm",
           "http://aup.hust.edu.cn/index/tzgg.htm",
           "http://ae.hust.edu.cn/index/xygg.htm",
           "http://mat.hust.edu.cn/bksjy/tzgg.htm",
           "http://chem.hust.edu.cn/bksjy/tzgg.htm"
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
               "物理学院",
               "管理学院",
               "社会学院",
               "土木学院",
               "公共管理学院",
               "生科院",
               "建规学院",
               "航空航天学院",
               "材料学院",
               "化学学院"
               ]
listtexts = []


def check_info():
    for index in range(len(listurl)):
        flag = False
        myURL = listurl[index]
        try:
            rep = request.urlopen(myURL).read()
        except urllib.error.HTTPError:
            print("打开{}网页失败，请手动进行检查".format(listschools[index]))
            break
        data = rep.decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")
        for tag in soup.find_all(text=re.compile("转专业|转入")):
            # if re.search("2021", tag.text, re.S):
            if tag.text not in listtexts:
                listtexts.append(tag.text)
                file = open(file="records.txt", encoding="utf8", mode="a")
                file.write(tag.text)
                file.write("\n")
                file.close()
                print(tag.text)
                flag = True
        if flag:
            print(listschools[index] + " 有新结果")
            make_notification(listschools[index])
    global Count
    Count += 1
    print("check for " + Count.__str__() + " times")
    timer = threading.Timer(60, check_info)
    timer.start()


def get_info():
    global listtexts
    if os.path.exists("records.txt"):
        file = open(file="records.txt", encoding="utf8", mode="r")
        listtexts = file.read().splitlines()
        for text in listtexts:
            print(text)
        file.close()
        return
    file = open(file="records.txt", encoding="utf8", mode="w")
    for index in range(len(listurl)):
        myURL = listurl[index]
        try:
            rep = request.urlopen(myURL).read()
        except urllib.error.HTTPError:
            print("打开{}网页失败，请手动进行检查")
            break
        data = rep.decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")
        for tag in soup.find_all(text=re.compile("转专业|转入")):
            listtexts.append(tag.text)
    for text in listtexts:
        file.write(text)
        file.write("\n")
        print(text)
    print("total: " + len(listtexts).__str__() + " records")
    file.close()


def make_notification(schoolname):
    notification_title = schoolname + "转专业消息有新结果"
    notification_message = "请到程序窗口查看"
    if platform.system() == 'Darwin':
        os.system(
            'osascript -e \'display notification "{}" with title "{}"\''.format(notification_message, notification_title))
        os.system('say {}'.format(notification_title))
    if platform.system() == 'Windows':
        notification = Notify()
        notification.title = notification_title
        notification.message = notification_message
        notification.send()


if __name__ == '__main__':
    get_info()
    check_info()
