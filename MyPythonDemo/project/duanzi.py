import requests  # 发起http请求
from bs4 import BeautifulSoup  # 解析html和xml


class DZ():
    def __init__(self, url, pageIndex):  # 实例对象自身，相当于java 的this
        self.url = url + str(pageIndex);
        self.headers = {'User_Agent': 'Mozill/4.0(compatible; MSIE 6.0; Windows NT)'}

    def get_one_page_html(self):
        re = requests.get(self.url, self.headers)
        print(re)
        html = re.text
        return html;

    def get_all_h2(self):
        for i in range(1, 2):  # 获取当前页面所有源代码
            # 获取html源代码
            html = self.get_one_page_html()

            # 解析
            soup = BeautifulSoup(html, 'lxml')  # 既可以解析html，也可以解析xml

            # 查找所有h2标签
            all_h2 = soup.find_all('h2')

        return all_h2

    def get_content(self):
        # <h2><a href="http://duanziwang.com/2785.html" title="6点见面-段子网">6点见面</a></h2>
        all_a = []
        all_title = []

        all_h2 = self.get_all_h2()
        for h2 in all_h2:
            all_a.append(h2.find('a').get('href'))
            all_title.append(h2.find('a').get('title'))

        for(title,a) in zip(all_title,all_a):

            print(title)

            with open('joke.txt','a+',encoding='utf-8') as file:   #上下文件管理器   a+ 追加模式
                file.write('标题:'+title[:-4]+"\n")

            re = requests.get(a,self.headers)
            html = re.text;
            soup = BeautifulSoup(html,'lxml')
            all_p = soup.find('article',class_='article-content').find_all('p')
            for p in all_p:
                with open('joke.txt','a+',encoding='utf-8') as files:
                    files.write(p.text+"\n")




if __name__ == '__main__':
    url = 'http://duanziwang.com/category/duanzi/page/'
    for i in range(1,4):
        app = DZ(url,i)
        app.get_content()
