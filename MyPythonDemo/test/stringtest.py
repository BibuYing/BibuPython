import time

# 获取文件名后缀
url = "http://www.mm36d.com/pic/small/20170301/1488336733764.jpg"
suffix = url.split(".")[-1]
print(suffix)

# 根据链接获取文件名
name = url.split("/")[-1]
print(name)

new_belle_list = [];
title = "title"
content = "content"
new_belle_list.append([title, content])
new_belle_list.append([title, content])
new_belle_list.append([title, content])
print(new_belle_list)

a = [1, 2, 3]
b = [2, 4, 5]
print(a + b)




# def aaa():
#     for num in range(1, 10):
#         if num == 4:
#
#             print("---")
#             break
#
#
#         print(str(num))
#
#
# aaa()

