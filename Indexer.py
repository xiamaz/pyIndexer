import os
import re

class FileCrawler:
    def __init__(self, home):
        self.home = home

    def getFiles(self):
        filelist = os.listdir(self.home)
        return filelist


class FileQuery:
    def __init__(self, expression):
        self.exp = re.compile(expression)

    def crawl(self, data):
        result = []
        for d in data:
            if self.exp.search(d):
                result.append(d)
        return result

    def fileList(self, data):
        filteredData = self.crawl(data)
        print(filteredData)
        result = map(lambda x: self.exp.sub("",d), filteredData)
        return result

class FileChanger:
    def __init__(self, orig, target):
        self.orig = FileQuery(orig)
        self.target = FileQuery(target)

    def changeList(self, data):
        origList = self.orig.fileList(data)
        newList = self.target.fileList(data)
        result = filter(set(origList.__contains__, newList))
        return result

def main():
    crawler = FileCrawler(os.getcwd()+"/Testfiles")
    filelist = crawler.getFiles()
    search = FileQuery("\.test$")
    print("Results")
    for s in search.fileList(filelist):
        print(s)

if __name__ == "__main__":
    main()
