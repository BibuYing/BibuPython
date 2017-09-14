import requests  # 发起http请求
from bs4 import BeautifulSoup  # 解析html和xml
from datetime import *
import time


class MR():
    def __init__(self, url):
        self.url = url;
        self.headers = {'User_Agent': 'Mozill/4.0(compatible; MSIE 6.0; Windows NT)'}

    def get_content(self):
        re = requests.get(self.url, self.headers)
        html = re.content.decode("utf8", "ignore")

        soup = BeautifulSoup(html, 'lxml')
        find_all = soup.find_all("table")

        for table in find_all:
            # print(table.find('tbody').find("tr").find("td").find(""))
            table_find_all = table.find_all('tr')

            td = table_find_all[1].find_all('td')

            date = td[0].string
            question = td[1].string
            answer = td[2].string

            print(date)
            print(question)
            print(answer)

            # date = td[0].find();
            # print(date)

            # 将9月12日 转成 2017-09-12
            print(time.strptime(date, "%m月%d日"))
            strptime = time.strptime(date, "%m月%d日")
            print(time.strftime(str(datetime.now().year) + "-%m-%d", strptime))


if __name__ == '__main__':
    url = 'http://app.3987.com/gonglue/16917.html'
    app = MR(url);
    app.get_content()
    input("按任意键退出")
