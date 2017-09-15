import os
import time


def dirlist(path):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)

        if os.path.isdir(filepath):
            dirlist(filepath)
        else:

            new = os.path.join(os.path.split(filepath)[0],
                               str(round(time.time() * 1000)) + os.path.splitext(filepath)[1])
            print(new)
            os.rename(filepath,new)
            time.sleep(0.001)


if __name__ == '__main__':
    dirlist("F:/图片/belle")
