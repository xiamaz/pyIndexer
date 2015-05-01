import os
import re


class FileCrawler:
    def __init__(self, home):
        self.home = home

    def changePath(self, newpath):
        self.home = newpath

    def getFiles(self):
        filelist = os.listdir(self.home)
        return filelist


class FileQuery:
    def __init__(self, expression):
        self.exp = re.compile(expression)

    def changeExpr(self, expr):
        self.exp = re.compile(expr)

    def crawl(self, data):
        # return a list of files filtered by the expression in class
        result = []
        for d in data:
            if self.exp.search(d):
                result.append(d)
        return result

    def fileList(self, data):
        # remove the file extension of crawl result, accept same data as crawl
        filteredData = self.crawl(data)
        print(filteredData)
        result = map(lambda x: self.exp.sub("", x), filteredData)
        return result


class FileChanger:
    def __init__(self, orig, target):
        self.orig = FileQuery(orig)
        self.target = FileQuery(target)

    def changeExpr(self, old, new):
        self.orig.changeExpr(old)
        self.target.changeExpr(new)

    def changeList(self, data, missing=True):
        origlist = self.orig.fileList(data)
        newlist = self.target.fileList(data)
        if missing:
            result = set(origlist).difference(newlist)
        else:
            result = set(origlist).intersection(newlist)
        return result

    def showOld(self, data):
        return self.orig.fileList(data)

    def linkFiles(self, fileiter):
        pass
        # create windows symbolic links save for later when ready for windows


def main():
    crawler = FileCrawler(os.getcwd()+"/Testfiles")
    filelist = crawler.getFiles()
    search = FileQuery("\.test$")
    print("Results")
    for s in search.fileList(filelist):
        print(s)

    print("FileChanger Results")
    changer = FileChanger('\.test$', '\.new$')
    for s in changer.changeList(filelist):
        print(s)


if __name__ == "__main__":
    main()
