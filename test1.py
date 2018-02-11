from bs4 import  BeautifulSoup
import  requests

url = "http://ring.itools.cn/"
html = requests.get(url)
soup = BeautifulSoup(html.text,"lxml")

songnames = soup.select('.sound h2')
playaddrs = soup.select('.sound_play')
i = 0
for songname , playaddr in zip(songnames,playaddrs):
    data = {
        '歌名':songname.text,
        '地址':playaddr.get('lurl')
    }
    print(data['歌名'],data['地址'])
    i = i+1
    print(i)

