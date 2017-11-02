import os
from PIL import Image
import shutil

# 图标参数
file_list = {"mipmap-mdpi": 48, "mipmap-hdpi": 72, "mipmap-xhdpi": 96, "mipmap-xxhdpi": 144, "mipmap-xxxhdpi": 192}
# 图标名称
icon_name = "ic_launcher.png"

# 圆形图标
round_icon_name = "ic_launcher_round.png"
# 是否需要删除圆形图标
delete_rount_icon = True;

# 当前路径
root_path = os.getcwd()
# 图标路径
icon_dir = os.path.join(root_path, "icon")


def delete():
    for dir, size in file_list.items():
        imageDirPath = os.path.join(root_path, dir);
        # 文件夹是否存在
        if os.path.exists(imageDirPath):
            listdir = os.listdir(imageDirPath)
            # 删除旧图标
            if icon_name in listdir:
                os.remove(os.path.join(imageDirPath, icon_name))
            # 删除圆形图标
            if round_icon_name in listdir and delete_rount_icon:
                os.remove(os.path.join(imageDirPath, round_icon_name))

        else:
            os.makedirs(imageDirPath)

        imagePath = get_image_path(size)
        if imagePath:
            # 移动文件
            os.rename(imagePath, os.path.join(imagePath, os.path.join(imageDirPath, icon_name)))


# 检查文件是否存在
def check_icon_dir():
    if os.path.exists(icon_dir):
        if (len(os.listdir(icon_dir)) > 0):
            return True
    return False


# 根据大小，提供图标路径
def get_image_path(size):
    for filename in os.listdir(icon_dir):
        if "PNG" in filename or "png" in filename:
            image = Image.open(os.path.join(icon_dir, filename))
            if size in image.size:
                return os.path.join(icon_dir, filename)
    return None


if __name__ == '__main__':
    if (check_icon_dir()):
        delete()
        # 完成后删除icon文件夹
        shutil.rmtree(icon_dir)
