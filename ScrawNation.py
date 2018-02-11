from bs4 import BeautifulSoup
import requests
import json
import pandas
import re


"""
案例：使用BeautifulSoup4
使用BeautifulSoup4解析器：
爬取旅游网站 时间、内容
"""

from bs4 import BeautifulSoup
import requests
import json

# 创建一个爬虫类
class LocationSpider():
    """
    一个爬虫类：爬取旅游网站页面信息
    """

    def __init__(self,url_front,url_end):
        """
        初始化函数
        :return:
        """
        # User-Agent头
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}

        self.url_front = url_front
        self.url_end = url_end
        self.file_name = open("my_nation.txt", "a+", encoding="utf-8")
        # 爬虫开始工作
        self.run()

    def run(self):
        """
        爬虫开始工作
        :return:
        """
        # 首页
        start_page = 1
        # 尾页
        end_page = self.getLastPage(self.url_front+str(0)+self.url_end)
        #print('end_page:::::'+str(end_page))
        # 循环处理每一页
        for page in range(start_page, 2):#: end_page + 1):
            print("正在处理第" + str(page) + "页")
            # 每一页有10个信息
            pn = (page - 1) * 30
            # 接接成完整的url地址
            full_url = self.url_front + str(pn) + self.url_end
            print('full url is :'+full_url)
            # 获取招聘详情链接:l square
            self.getInfo(full_url)
        # 关闭文件
        self.file_name.close()

    def getLastPage(self, url):
        """
        获取尾页的page值
        :param url: 首页的url地址
        :return: 尾页的page值
        """
        print('pageurl:'+url)
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "lxml")
            page = soup.find_all("a", attrs={"class": "pageNum taLnk"})[-1]
            page = page.get('data-page-number')
            #page = page_nav.find_all('pageNum taLnk')[-1].text
            # print(page)
            # print('page:'+page)
            return int(page)

        except:
            # 若异常、则舍弃这条信息
            pass






    def getInfo(self, url):
        """
        获取我们需爬取的信息
        :param url: 招聘详情页面
        :return: None
        """
        print('info:'+url)
        # 获取url页面的内容：bytes
        try:
            html = requests.get(url)
            # 创建 Beautiful Soup 对象，指定lxml解析器
            soup = BeautifulSoup(html.text, "lxml")
        except:
            pass
            return

        try:
            infos = soup.find_all("div",attrs={"class": "listing_title"})#.find_all(name='a')
            print(infos)
            # print(infos.find("a").text)

            for info in (infos):
                data = {
                    'title' : info.find("a").text,
                    'url'   : 'https://www.tripadvisor.com'+ info.find("a").get("href")
                    #'location_url': location_url.text
                }
                # 保存这条记录
                if data:
                    line = json.dumps(data, ensure_ascii=False) + "\n"
                    self.file_name.write(line)
                    print(data)
                else:
                    print('data is null')
        except:
            # 若异常、则舍弃这条信息
            print('fffffff')
            pass


# 主函数
if __name__ == '__main__':
    #URLs= pandas.read_csv('trip.csv',usecols=[4],header=0)
    URLs ='https://www.tripadvisor.com/Attractions-g294265-Activities-Singapore.html'
    #https: // www.tripadvisor.com / Attractions - g294265 - Activities - oa30 - Singapore.html  # FILTERED_LIST
    #URL = pandas.read_csv('trip.csv', usecols=[4], header=0)
    str_target = 'Activities-'
    for index in range (1):#(len(URLs)):
        #url = URLs.values[index]
        #url = str(url)
        url = URLs
        i = url.find(str_target)
        url_front = url[0:i + 11] + 'oa'
        url_end = url[i + 10:]
        print('front:'+url_front)
        print('end:'+url_end)
        print(url_front + url_end)
        my_spider = LocationSpider(url_front, url_end)
        print('the ' + str(index) + 'location_url finished')
