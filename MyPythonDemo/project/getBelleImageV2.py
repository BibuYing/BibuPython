import os

import requests
from bs4 import BeautifulSoup
import time

MODE_ADD = "add"  # 追加模式
MODE_ALL = "all"  # 全盘扫描模式

# 获取网站图片
main_path = "http://mm36d.com/home/0/"
detail_path = "http://mm36d.com/belle/0/0/%s/2"
result_root_path = 'F:/图片/belle/'


class Belle:
    def __init__(self, mode):
        self.mode = mode

    def begin(self):
        position = 1

        new_belle_list = [];

        while True:
            url = main_path + str(position)

            belle_list_html = self.getHtml(url)
            state = self.get_belle_list(belle_list_html, new_belle_list)

            if state:
                position += 1
            else:
                break

        for belle_detail in new_belle_list:
            print("更新资源---" + belle_detail[0] + "------" + belle_detail[1])
            #
            self.getDetail(belle_detail[0], belle_detail[1])

    # 获取主题详情
    def getDetail(self, dirName, url):
        print("==============================================================================")
        html = self.getHtml(url)
        soup = BeautifulSoup(html, "lxml")
        div = soup.find("div", class_="body-cont").find("div", class_="container").find("div", class_="grid_v")
        li_list = div.find_all('li', class_="re-sizemm")

        if not li_list or len(li_list) <= 0:
            return

        path = result_root_path + "/" + dirName
        self.createFolder(path)

        for li in li_list:
            imageUrl = li.find('img').get('data-original')
            fileName = path + "/" + self.getFileName(imageUrl)
            self.downLoadImage(imageUrl, fileName)

    def get_belle_list(self, html, new_belle_list):
        if not html:
            print("请求数据为空")
            return False

        soup = BeautifulSoup(html, "lxml")
        div = soup.find('div', class_="grid_v")
        li_list = div.find_all('li', class_="col-md-3 re-size1")

        if not li_list or len(li_list) <= 0:
            print("列表不存在")
            return False

        for li in li_list:
            a = li.find('a')
            id = str(a.get('onclick')).replace("lookmm(", "").replace(")", "")
            url = detail_path % id
            title = a.string.replace("(点击图片,更多精彩)", "").strip()
            # 追加模式且目录以及存在，就不再遍历
            if self.isExist(result_root_path + title):
                if self.mode == MODE_ADD:
                    return False
                else:
                    continue
            else:
                new_belle_list.append([title, url])

        return True

    def getHtml(self, url):
        print("加载链接:" + url)
        cookies = dict(
            comefrom='mm36d'
        )
        s = requests.Session()
        response = s.get(url, allow_redirects=True, cookies=cookies)
        if response.status_code == 200:
            return response.text
        else:
            return None

    # 创建文件夹
    def createFolder(self, dirPath):
        if not self.isExist(dirPath):
            os.makedirs(dirPath)
            return True
        else:

            return False

    # 是否已存在
    def isExist(self, path):
        return os.path.exists(path)

    # 根据链接获取文件名
    def getFileName(self, url):
        FileName = url.split("/")[-1]
        return self.rename(FileName)

    # 将文件名采用时间戳进行重命名
    def rename(self, FileName):
        name = str(round(time.time() * 1000))
        suffix = FileName.split(".")[-1]
        return name + "." + suffix

    # 下载图片
    def downLoadImage(self, imageUrl, fileName):
        print("开始下载：" + imageUrl)

        if not os.path.exists(fileName):
            # time.sleep(1)
            # 下载图片
            response = requests.get(imageUrl)
            # 创建图片
            image_file = open(fileName, "wb")
            # 写入图片
            image_file.write(response.content)

            image_file.close()  # 关闭文件
            response.close()  # 关闭请求
            print("已下载到：" + fileName)
        else:
            print("文件已存在：" + fileName)


if __name__ == '__main__':
    app = Belle(MODE_ADD)
    app.begin()
