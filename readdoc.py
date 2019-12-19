import os
import shutil

path = "E:/test"  # 文件夹目录
files = os.listdir(path)  # 得到文件夹下的所有文件名称
epubBookNames = []
mobiBookNames = []
azw3BookNames = []
for file in files:  # 遍历文件夹
    subFolder = path + "/" + file
    bookNames = []
    if os.path.isdir(subFolder):
        sf = os.listdir(subFolder)
        for sfd in sf:
            bookNames.append(subFolder + "/" + sfd)
    for bookName in bookNames:
        if os.path.splitext(bookName)[-1] == '.epub':
            epubBookNames.append(bookName)
        if os.path.splitext(bookName)[-1] == '.mobi':
            mobiBookNames.append(bookName)
        if os.path.splitext(bookName)[-1] == '.azw3':
            azw3BookNames.append(bookName)
for mobi in mobiBookNames:
    for epub in epubBookNames:
        if os.path.splitext(mobi)[0] == os.path.splitext(epub)[0]:
            os.remove(epub)
        elif os.path.splitext(mobi)[0]+"(1)" == os.path.splitext(epub)[0]:
            os.remove(epub)
    for azw3 in azw3BookNames:
        if os.path.splitext(mobi)[0] == os.path.splitext(azw3)[0]:
            os.remove(azw3)
        elif os.path.splitext(mobi)[0] + "(1)" == os.path.splitext(azw3)[0]:
            os.remove(azw3)
    if mobi:
        shutil.move(mobi, path)
for file in files:
    subFolder = os.path.isdir(path + "/" + file)
    if subFolder:
        sf = os.listdir(path + "/" + file)
        if sf:
            print('不空')
        else:
            print("空")
            os.rmdir(path + "/" + file)
