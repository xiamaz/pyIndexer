import Indexer

# adding functions to be executed on user interaction


class Controller:
    def __init__(self, workingdir="/home/max/Gits/pyIndexer/Testfiles",
                 oldname=".test", newname=".new"):
        self.crawler = Indexer.FileCrawler(workingdir)
        oldexp = "\\{}$".format(oldname)
        newexp = "\\{}$".format(newname)
        self.changer = Indexer.FileChanger(oldexp, newexp)

        self.crawlDir()

    def changeExpr(self, old, new):
        self.changer.changeExpr(old, new)

    def changeDir(self, newdir):
        self.crawler.changePath(newdir)

    def crawlDir(self):
        self.data = self.crawler.getFiles()

    def getAll(self):
        filelist = self.changer.showOld(self.data)
        return filelist

    def getNew(self):
        filelist = self.changer.changeList(self.data, missing=False)
        return filelist

    def getOld(self):
        filelist = self.changer.changeList(self.data, missing=True)
        return filelist

    def copyFiles(self):
        pass


if __name__ == '__main__':
    print("Testing the UI Interaction functions")
