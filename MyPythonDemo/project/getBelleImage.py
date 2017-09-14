import os

import requests
from bs4 import BeautifulSoup

main_path = "http://mm36d.com/home/0/"
detail_path = "http://mm36d.com/belle/0/0/%s/2"
result_root_path = 'E:/belle/'

max_position = 75;


def main():
    createFolder(result_root_path)

    position = 1

    while position <= max_position:
        print("+++++++++++++++第" + str(position) + "页++++++++++++++++++++++")
        html = getHtml(main_path + str(position))
        getBelleList(html)
        position += 1


# 获取主题列表
def getBelleList(html):
    soup = BeautifulSoup(html, "lxml")
    div = soup.find('div', class_="grid_v")
    li_list = div.find_all('li', class_="col-md-3 re-size1")

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
    createFolder(path)
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
def createFolder(fileName):
    if not os.path.exists(fileName):
        os.makedirs(fileName)
        print(fileName + "---已创建")
    else:
        print(fileName + "---已存在")


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


# 根据链接获取文件名
def getFileName(url):
    return url.split("/")[-1]


if __name__ == '__main__':
    main()