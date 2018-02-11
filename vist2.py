"""
案例：使用BeautifulSoup4爬取腾讯招聘页面的数据
使用BeautifulSoup4解析器：
爬取旅游网站 时间、内容
"""

from bs4 import BeautifulSoup
import requests
import json


# 创建一个爬虫类
class VistSpider(object):
    """
    一个爬虫类：爬取旅游网站页面信息
    """

    def __init__(self):
        """
        初始化函数
        :return:
        """
        # User-Agent头
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}

        self.url_front = "https://www.tripadvisor.com/Attraction_Review-g303631-d553566-Reviews-or"
        self.url_end = "-Catedral_da_Se_de_Sao_Paulo-Sao_Paulo_State_of_Sao_Paulo.html"
        self.file_name = open("visit.txt", "w", encoding="utf-8")

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
        #end_page =27
        print('end_page',end_page)
        # 循环处理每一页
        for page in range(start_page, end_page + 1):
            print("正在处理第" + str(page) + "页")
            # 每一页有10个信息
            pn = (page - 1) * 10
            # 接接成完整的url地址
            full_url = self.url_front + str(pn) + self.url_end
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

        html = requests.get(url)
        print(html.text)
        soup = BeautifulSoup(html.text, "lxml")
        print(soup.text)
        page_nav = soup.select('div[class="pageNumbers"]')[0]
        page = page_nav.find_all('span')[-1].text
        print(page)

        return int(page)



    def getInfo(self, url):
        """
        获取我们需爬取的信息
        :param url: 招聘详情页面
        :return: None
        """
        # 获取url页面的内容：bytes
        html = requests.get(url)
        # 创建 Beautiful Soup 对象，指定lxml解析器
        soup = BeautifulSoup(html.text, "lxml")

        try:
            dates = soup.select('div[class="rating reviewItemInline"]')
            comments = soup.select('div[class="entry"]')
            for date, comment in zip(dates, comments):
                data = {
                    'time': date.select('span[class="ratingDate relativeDate"]')[0].text,
                    'comment': comment.text
                }
                # 保存这条记录
                if data:
                    line = json.dumps(data, ensure_ascii=False) + "\n"
                    self.file_name.write(line)
        except:
            # 若异常、则舍弃这条信息
            pass


# 主函数
if __name__ == '__main__':
    my_spider = VistSpider()