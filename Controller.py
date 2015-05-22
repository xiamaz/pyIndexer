import Indexer
import shutil

# adding functions to be executed on user interaction


class Controller:
    def __init__(self, workingdir="/home/max/Gits/pyIndexer/Testfiles",
                 oldname=".test", newname=".new"):
        self.crawler = Indexer.FileCrawler(workingdir)
        oldexp = "\\{}$".format(oldname)
        newexp = "\\{}$".format(newname)
        self.oldname = oldname
        self.newname = newname
        self.changer = Indexer.FileChanger(oldexp, newexp)

        self.crawlDir()

    def changeExpr(self, old, new):
        self.oldname = old
        self.newname = new
        oldf = "\\{}$".format(old)
        newf = "\\{}$".format(new)
        self.changer.changeExpr(oldf, newf)

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

    def linkFiles(self):
        path = self.crawler.home
        print(path)
        data = self.getOld()
        for d in data:
            old = path+'\\'+d+self.oldname
            print(old)
            new = path+'\\'+d+self.newname
            print(new)
            shutil.copyfile(old, new)


if __name__ == '__main__':
    print("Testing the UI Interaction functions")
    control = Controller("C:\\Users\\admin\\Git\\pyIndexer\\Testfiles")
    control.crawlDir()
    control.getOld()
    control.linkFiles()

