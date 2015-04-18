# -*- encoding:utf-8 -*-

import urllib2
import urllib
import re
import thread
import time

class Spider_Model:

    def __init__(self):

        self.page = 200
        self.pages = []
        self.enable = False
        print u"请输入想开始的页数（默认将从第%d页开始）：" % self.page
        temp_page = raw_input()
        if temp_page.isdigit():
            self.page = int(temp_page)

    # 将所有的段子都添加到列表中并且返回列表
    def GetPage(self, page):

        myUrl = "http://jandan.net/duan/page-" + page + "#comments"
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        headers = {'User-Agent' : user_agent}
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()

        unicodePage = myPage.decode('utf-8')

        # re.s是任意匹配模式，也就是.可以匹配换行符
        pattern ='<div.*?class="text"><span.*?class=".*?"><a.*?href=".*?">.*?</a>' + \
            '</span><p>(.*?)</p>\s+<div.*?class="vote".*?cos_support-.*?">(\d+)</span>.*?cos_unsupport-.*?">(\d+)</span>]</div>'
        myItems = re.findall(pattern, unicodePage, re.S)

        items = []

        # myItems中是包含一个页面内所有段子信息的list
        # 每一个元素是一个元组，依次为段子内容、oo数、xx数
        for item in myItems:
            text = item[0].replace("<br />", " ")
            items.append([text, item[1], item[2]])
        return items

    # 用于加载新的段子
    def LoadPage(self):
        # 如果用户未输入quit则一直运行
        while self.enable:
            # 如果pages数组中德内容小于2个
            if len(self.pages) < 2:
                try:
                    # 获取新的页面中的段子
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except:
                    print u"无法连接煎蛋段子"
            else:
                time.sleep(1)

    def ShowPage(self, nowPage, page):
        for items in nowPage:
            try:
                # 这里只显示oo数大于xx数的段子
                if int(items[1]) >= int(items[2]):
                    print "-"*80 + "\n"
                    print u"第%d页" % page, items[0]
                    print "\noo:" + items[1] + "\txx:" + items[2]
                    myInput = raw_input()
                    if myInput == "quit" or myInput == "q":
                        self.enable = False
                        break
            except:
                print u"这条段子无法正常显示……\n"

    def Start(self):
        self.enable = True
        page = self.page

        print u"正在加载中请稍候……"
        # 新建一个线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage, ())

        while self.enable:
            #如果self的pages数组中存有元素
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage, page)
                page += 1

# print u"请按下回车浏览今日的煎蛋段子……："
print u'''--------------------------------------------------
        程序功能：在命令行中浏览煎蛋网的段子
        Author: wukai
        Time: 2015-04-18
        输入回车读取更多，have fun!
--------------------------------------------------
'''
myModel = Spider_Model()
myModel.Start()

