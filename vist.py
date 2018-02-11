from bs4 import  BeautifulSoup
import  requests

# url_front = "https://www.tripadvisor.com/Attraction_Review-g303631-d553566-Reviews-or"
# url_end ="-Catedral_da_Se_de_Sao_Paulo-Sao_Paulo_State_of_Sao_Paulo.html"
# start_page=0
# i = 0
# while(start_page<=50):
#     url = url_front + str(start_page) + url_end
#     html = requests.get(url)
#     soup = BeautifulSoup(html.text, "lxml")
#     #
#     dates = soup.select('div[class="rating reviewItemInline"]')
#     # time = dates[0].select('span[class="ratingDate relativeDate"]')[0].text
#     # print(time)
#     comments = soup.select('div[class="entry"]')
#     # print(comments[0].text)
#     for date, comment in zip(dates, comments):
#         print(i)
#         data = {
#             'time': date.select('span[class="ratingDate relativeDate"]')[0].text,
#             'comment': comment.text
#         }
#         print(data['time'], data['comment'])
#         i = i + 1
#
#
#     start_page = start_page +10;

url_front = "https://www.tripadvisor.com/Attraction_Review-g303631-d553566-Reviews-or"
url_end ="-Catedral_da_Se_de_Sao_Paulo-Sao_Paulo_State_of_Sao_Paulo.html"
url = url_front + str(0) + url_end
html = requests.get(url)
soup = BeautifulSoup(html.text, "lxml")
print(soup)
page_nav = soup.select('div[class="pageNumbers"]')[0]
# print(page_nav)
page = page_nav.find_all('span')[-1].text
print(page)