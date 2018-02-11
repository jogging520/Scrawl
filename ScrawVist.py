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
class VistSpider():
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
        self.file_name = open("my_visit.txt", "a+", encoding="utf-8")
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
        # 循环处理每一页
        for page in range(start_page, end_page + 1):
            print("正在处理第" + str(page) + "页")
            # 每一页有10个信息
            pn = (page - 1) * 10
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
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "lxml")
            page_nav = soup.select('div[class="pageNumbers"]')[0]
            page = page_nav.find_all('span')[-1].text
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
        # 获取url页面的内容：bytes
        try:
            html = requests.get(url)
            # 创建 Beautiful Soup 对象，指定lxml解析器
            soup = BeautifulSoup(html.text, "lxml")
        except:
            pass
            return

        try:
            key_views = soup.select('span[class="ui_tagcloud fl"]')
            total = soup.select('span[class="reviews_header_count block_title"]')
            user_ids = soup.select('span[class="expand_inline scrname"]')
            dates = soup.select('div[class="rating reviewItemInline"]')
            notes = soup.select('span[class="noQuotes"]')
            comments = soup.select('div[class="entry"]')
            supports = soup.select('span[class="badgetext"]')
            # if(len(key_views)!=0):
            #     print("++++++++++++++++++"+key_views[0].text)
            #print('key++++++++++++++++:'+total)
            for user_id,date,note,comment,support in zip(user_ids,dates,notes,comments,supports):
                data = {
                    #'view' : all_view.text,
                    'location': url_end[1:-4],
                    'total_number': total[0].text,
                    #'key_views':key_views[0].text,
                    'user_id': user_id.text,
                    'time': date.select('span[class="ratingDate relativeDate"]')[0].text,
                    'note': note.text,
                    'comment': comment.text,
                    'support': support.text
                }
                # 保存这条记录
                if data:
                    line = json.dumps(data, ensure_ascii=False) + "\n"
                    self.file_name.write(line)
                    print(data)
        except:
            # 若异常、则舍弃这条信息
            pass


# 主函数
if __name__ == '__main__':
    URLs= pandas.read_csv('trip.csv',usecols=[4],header=0)
    str_target = 'Reviews-'
    for index in range(len(URLs)):
        url = URLs.values[index]
        url = str(url)
        i = url.find(str_target)
        url_front = url[3:i+ 8] + 'or'
        url_end = url[i+ 7:-2]
        print(url_front+url_end)
        my_spider = VistSpider(url_front, url_end)
        print('the'+str(index)+'location_url finished')