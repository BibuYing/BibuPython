import os

import requests
from bs4 import BeautifulSoup
import time


# 获取网站图片
main_path = "http://mm36d.com/home/0/"
detail_path = "http://mm36d.com/belle/0/0/%s/2"
result_root_path = 'E:/belle/'



exitsPass = True  # 当爬取到链接存在时候直接关闭脚本，用于日常增量更新


def main():
    createFolder(result_root_path)

    position = 77

    while True:
        print("+++++++++++++++第" + str(position) + "页++++++++++++++++++++++")
        html = getHtml(main_path + str(position))
        if getBelleList(html):
            position += 1
        else:
            print("列表不存在...")
            break


# 获取主题列表
def getBelleList(html):
    soup = BeautifulSoup(html, "lxml")
    div = soup.find('div', class_="grid_v")
    li_list = div.find_all('li', class_="col-md-3 re-size1")

    if not li_list or len(li_list) <= 0:
        print("列表不存在")
        return False

    for li in li_list:
        # time.sleep(3)
        a = li.find('a')
        id = str(a.get('onclick')).replace("lookmm(", "").replace(")", "")
        url = detail_path % id
        title = a.string.replace("(点击图片,更多精彩)", "").strip()
        path = result_root_path + title
        getDetail(url, path)


# 获取主题详情
def getDetail(detailUrl, path):
    print("==============================================================================")

    if not createFolder(path):
        return

    print("详情页:", detailUrl)
    html = getHtml(detailUrl)
    soup = BeautifulSoup(html, "lxml")
    div = soup.find("div", class_="body-cont").find("div", class_="container").find("div", class_="grid_v")
    li_list = div.find_all('li', class_="re-sizemm")
    for li in li_list:
        imageUrl = li.find('img').get('data-original')
        fileName = path + "/" + getFileName(imageUrl)
        downLoadImage(imageUrl, fileName)


def getHtml(url):
    print(url)
    cookies = dict(
        comefrom='mm36d'
    )
    s = requests.Session()
    response = s.get(url, allow_redirects=True, cookies=cookies)
    html = response.text
    return html


# 创建文件夹
def createFolder(dirPath):
    if not isExist(dirPath):
        os.makedirs(dirPath)
        return True
    else:
        print(dirPath + "---目录已存在")
        return False


# 是否已存在
def isExist(path):
    return os.path.exists(path)


# 根据链接获取文件名
def getFileName(url):
    FileName = url.split("/")[-1]
    return rename(FileName)


# 将文件名采用时间戳进行重命名
def rename(FileName):
    name = str(round(time.time() * 1000))
    suffix = FileName.split(".")[-1]
    return name + "." + suffix


# 下载图片
def downLoadImage(imageUrl, fileName):
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
    main()
