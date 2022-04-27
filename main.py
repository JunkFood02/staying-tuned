import os
import urllib.error
from urllib import request

import threading
import platform
import re
from notifypy import Notify
from bs4 import BeautifulSoup

Count = 0
schoolUrlDictionary = {
    "教务处": "http://jwc.hust.edu.cn/",
    "软件学院": "http://sse.hust.edu.cn/tztg.htm",
    "法医学院": "http://fayixi.tjmu.edu.cn/rcpy1/bksjy/jxdt.htm",
    "口腔医学院": "http://stomatology.hust.edu.cn/xwzx/gsl.htm",
    "网络安全学院": "http://cse.hust.edu.cn/index.htm",
    "计算机学院": "http://www.cs.hust.edu.cn/",
    "机械学院": "http://mse.hust.edu.cn/sylm/tzgg.htm",
    "光电学院": "http://oei.hust.edu.cn/ywtz.htm",
    "第二临床学院": "https://www.tjh.com.cn/channels/290.html",
    "人文学院": "http://humanity.hust.edu.cn/tzgg.htm",
    "经济学院": "http://eco.hust.edu.cn/index.htm",
    "电气学院": "http://seee.hust.edu.cn/xwzx/tzgg.htm",
    "电信学院": "http://ei.hust.edu.cn/index.htm",
    "外国语学院": "http://sfl.hust.edu.cn/bkjx/jxtz.htm",
    "数学学院": "http://maths.hust.edu.cn/index/tzgg.htm",
    "自动化学院": "http://aia.hust.edu.cn/tzgg/bks.htm",
    "物理学院": "http://phys.hust.edu.cn/rcpy/bksjy/tzgg.htm",
    "管理学院": "http://cm.hust.edu.cn/old/bk/jwgg.htm",
    "社会学院": "http://soci.hust.edu.cn/bksjy/tzgg.htm",
    "土木学院": "http://civil.hust.edu.cn/index/tzgg.htm",
    "公共管理学院": "http://cpa.hust.edu.cn/zsjx/bks/jwxx.htm",
    "生科学院": "http://life.hust.edu.cn/tzgg/bksjy.htm",
    "建规学院": "http://aup.hust.edu.cn/index/tzgg.htm",
    "航空航天学院": "http://ae.hust.edu.cn/index/xygg.htm",
    "材料学院": "http://mat.hust.edu.cn/bksjy/tzgg.htm",
    "化学学院": "http://chem.hust.edu.cn/bksjy/tzgg.htm"
}
listurl = ["http://jwc.hust.edu.cn/",
           "http://sse.hust.edu.cn/tztg.htm",
           "http://fayixi.tjmu.edu.cn/rcpy1/bksjy/jxdt.htm",
           "http://stomatology.hust.edu.cn/xwzx/gsl.htm",
           "http://cse.hust.edu.cn/index.htm",
           "http://www.cs.hust.edu.cn/",
           "http://mse.hust.edu.cn/sylm/tzgg.htm",
           "http://oei.hust.edu.cn/ywtz.htm",
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
    for school in schoolUrlDictionary.keys():
        flag = False
        myURL = schoolUrlDictionary[school]
        try:
            rep = request.urlopen(myURL).read()
        except urllib.error.HTTPError:
            print("打开{}网页失败，请手动进行检查".format(school))
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
            print(school + " 有新结果")
            make_notification(school)
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
    for school in schoolUrlDictionary.keys():
        myURL = schoolUrlDictionary[school]
        try:
            rep = request.urlopen(myURL).read()
        except urllib.error.HTTPError:
            print("打开{}网页失败，请手动进行检查".format(school))
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
            'osascript -e \'display notification "{}" with title "{}"\''.format(notification_message,
                                                                                notification_title))
        os.system('say {}'.format(notification_title))
    if platform.system() == 'Windows' or 'Linux':
        notification = Notify()
        notification.title = notification_title
        notification.message = notification_message
        notification.send()


if __name__ == '__main__':
    get_info()
    check_info()
