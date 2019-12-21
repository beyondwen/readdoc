import hashlib
import os
import shutil

path = "D:/BaiduNetdiskDownload"  # 文件夹目录
files = os.listdir(path)  # 得到文件夹下的所有文件名称
epubBookNames = []
collatedEpubBookNames = []
mobiBookNames = []
collatedMobiBookNames = []
azw3BookNames = []
collatedAzw3BookNames = []
bookDict = {}
collatedBookDict = {}
bookSha1s = []


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        return sha1obj.hexdigest()


def CalcStringSha1(text):
    text = text.encode()
    sha1obj = hashlib.sha1()
    sha1obj.update(text)
    return sha1obj.hexdigest()


def CalcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()


def addDict(file):
    bookCache = []
    sha1Value = CalcSha1(file)
    bookSha1s.append(sha1Value)
    bookCache.append(file)
    mv = bookDict.get(sha1Value)
    if mv:
        mv.append(file)
    else:
        bookDict[sha1Value] = bookCache
    return bookDict, bookSha1s


def forEachFile(bookFiles):
    bookSha1s.clear()
    bookDict.clear()
    for bookFile in bookFiles:
        bookFileDict, bookSha1sList = addDict(bookFile)
    return bookFileDict, bookSha1sList


def statisticsSameFile(files):
    bookFileDict, bookSha1sList = forEachFile(files)
    bookSha1sList1 = list(set(bookSha1sList))
    for bookSha1 in bookSha1sList1:
        mv = bookFileDict.get(bookSha1)
        mv.sort()
        for cmv in mv:
            if cmv == mv[-1]:
                if os.path.splitext(cmv)[-1] == '.epub':
                    collatedEpubBookNames.append(cmv)
                if os.path.splitext(cmv)[-1] == '.mobi':
                    collatedMobiBookNames.append(cmv)
                if os.path.splitext(cmv)[-1] == '.azw3':
                    collatedAzw3BookNames.append(cmv)
            else:
                os.remove(cmv)


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

book = [epubBookNames, mobiBookNames, azw3BookNames]
for b in book:
    statisticsSameFile(b)


def cacheCollatedBook(bookName, cb):
    collatedBookCache = []
    h1 = CalcStringSha1(bookName)
    cbd = collatedBookDict.get(h1)
    if cbd:
        cbd.append(cb)
        collatedBookDict[h1] = cbd
    else:
        collatedBookCache.append(cb)
        collatedBookDict[h1] = collatedBookCache


collatedBook = [collatedMobiBookNames, collatedAzw3BookNames, collatedEpubBookNames]
for collatedbook in collatedBook:
    for cb in collatedbook:
        sbt = cb.split("/")
        if os.path.splitext(sbt[3])[-1] == '.epub':
            epubBookNames.append(sbt[3])
            cacheCollatedBook(os.path.splitext(sbt[3])[0], cb)
        if os.path.splitext(sbt[3])[-1] == '.mobi':
            mobiBookNames.append(sbt[3])
            cacheCollatedBook(os.path.splitext(sbt[3])[0], cb)
        if os.path.splitext(sbt[3])[-1] == '.azw3':
            azw3BookNames.append(sbt[3])
            cacheCollatedBook(os.path.splitext(sbt[3])[0], cb)

for cbd in collatedBookDict:
    cbList = collatedBookDict.get(cbd)
    if len(cbList) == 3:
        for cbl in cbList:
            shufxx = os.path.splitext(cbl[3])
            if (cbl.split("/")[3].split(".")[-1]) == "azw3":
                os.remove(cbl)
            if (cbl.split("/")[3].split(".")[-1]) == "epub":
                os.remove(cbl)
            if (cbl.split("/")[3].split(".")[-1]) == "mobi":
                shutil.move(cbl, path)
    if len(cbList) == 2:
        os.remove(cbList[1])
        shutil.move(cbList[0], path)
    if len(cbList) == 1:
        shutil.move(cbList[0], path)

for file in files:
    subFolder = os.path.isdir(path + "/" + file)
    if subFolder:
        sf = os.listdir(path + "/" + file)
        if sf:
            print('不空')
        else:
            print("空")
            os.rmdir(path + "/" + file)
