"""
案例：使用BeautifulSoup4爬取腾讯招聘页面的数据
url：http://hr.tencent.com/position.php?&start=10#a
使用BeautifulSoup4解析器，爬取每个招聘详情页面里面的：
职位名称、工作地点、职位类别、招聘人数、工作职责、工作要求、url链接
"""

from bs4 import BeautifulSoup
import urllib.request
import json


# 创建一个爬虫类
class TencentSpider(object):
    """
    一个爬虫类：爬取腾讯招聘页面信息
    """

    def __init__(self):
        """
        初始化函数
        :return:
        """
        # User-Agent头
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        self.url = "http://hr.tencent.com/"
        self.file_name = open("tencent.txt", "w", encoding="utf-8")

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
        end_page = self.getLastPage(self.url + "position.php?&start=0#a")
        # 循环处理每一页
        for page in range(start_page, end_page + 1):
            print("正在处理第" + str(page) + "页")
            # 每一页有10个招聘信息
            pn = (page - 1) * 10
            # 接接成完整的url地址
            full_url = self.url + "position.php?&start=" + str(pn) + "#a"
            # 获取招聘详情链接:l square
            link_list = self.getPositons(full_url)
            for link in link_list:
                # 拼接成完整的链接
                full_link = self.url + link
                # 获取招聘信息页面里的所需爬取的信息
                self.getPositionInfo(full_link)

        # 关闭文件
        self.file_name.close()

    def getLastPage(self, url):
        """
        获取尾页的page值
        :param url: 首页的url地址
        :return: 尾页的page值
        """
        # 获取url页面的内容：bytes
        html = self.loadPage(url)
        # bytes转utf-8
        html = html.decode("utf-8")
        # 创建 Beautiful Soup 对象，指定lxml解析器
        soup = BeautifulSoup(html, "lxml")
        page_nav = soup.select('div[class="pagenav"]')[0]
        page = page_nav.find_all('a')[-2].get_text()

        return int(page)

    def loadPage(self, url):
        """
        获取url页面的内容
        :param url: 需要获取内容的url地址
        :return: url页面的内容
        """
        # url 连同 headers，一起构造Request请求，这个请求将附带 chrome 浏览器的User-Agent
        request = urllib.request.Request(url, headers=self.header)
        # 向服务器发送这个请求
        response = urllib.request.urlopen(request)
        # time.sleep(3)
        # 获取网页内容：bytes
        html = response.read()

        return html

    def getPositons(self, url):
        """
        获取url页面内的招聘详情链接
        :param url:
        :return:
        """
        # 获取url页面的内容：bytes
        html = self.loadPage(url)
        # bytes转utf-8
        html = html.decode("utf-8")
        # 创建 Beautiful Soup 对象，指定lxml解析器
        soup = BeautifulSoup(html, "lxml")

        item_list = soup.select('td[class="l square"]')
        link_list = []
        for item in item_list:
            item = item.select('a')[0].attrs['href']
            link_list.append(item)

        return link_list

    def getPositionInfo(self, url):
        """
        获取我们需爬取的信息
        :param url: 招聘详情页面
        :return: None
        """
        # 获取url页面的内容：bytes
        html = self.loadPage(url)
        # bytes转utf-8
        html = html.decode("utf-8")
        # 创建 Beautiful Soup 对象，指定lxml解析器
        soup = BeautifulSoup(html, "lxml")
        # 用于存储所爬取信息的字典
        item = {}
        try:
            # 职位名称
            position_name = soup.find_all(id="sharetitle")[0].get_text()
            # 工作地点、职位类型、招聘人数
            bottomline = soup.select('tr[class="c bottomline"] td')
            # 工作地点
            working_place = bottomline[0].get_text()[5:]
            # 职位类别
            position_category = bottomline[1].get_text()[5:]
            # 招聘人数
            numbers = bottomline[2].get_text()[5:]
            # 工作职责
            operating_duty_list = soup.select('ul[class="squareli"]')[0].select('li')
            operating_duty = ""
            for duty in operating_duty_list:
                operating_duty += duty.get_text().strip() + "\n"
            # 工作要求
            requirements_list = soup.select('ul[class="squareli"]')[1].select('li')
            requirements = ""
            for requ in requirements_list:
                requirements += requ.get_text().strip() + "\n"
            # url链接
            url_links = url
            # 职位名称、工作地点、职位类别、招聘人数、工作职责、工作要求、url链接
            item["职位名称"] = position_name
            item["工作地点"] = working_place
            item["职位类别"] = position_category
            item["招聘人数"] = numbers
            item["工作职责"] = operating_duty
            item["工作要求"] = requirements
            item["url链接"] = url_links
        except:
            # 若异常、则舍弃这条信息
            pass
        # 保存这条记录
        if item:
            line = json.dumps(item, ensure_ascii=False) + "\n"
            self.file_name.write(line)


# 主函数
if __name__ == '__main__':
    my_spider = TencentSpider()