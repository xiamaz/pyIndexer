import Indexer
import Configuration
import os

# the controller implements the configuration on the indexer operations, all
# user interface commands pass through the controller


class Controller:
    def __init__(self, crawl):
        # initialize the Controller object, first we would need to initialize
        # the configuration system
        # the configuration is saved in the appdata system
        self.configuration = Configuration.Configuration(crawl=crawl)
        self.crawler = Indexer.FileCrawler()
        self.sep = os.sep

    def startConf(self):
        print("Start configuration process")
        status = self.configuration.startConf()
        return status

    def initConf(self, crawl):
        self.configuration.initialSetup(crawl)
        self.configuration.writeConfFile()

    def linkFile(self, selectedFile):
        origPath = self.configuration.getConfig("crawldir") + \
            os.sep + selectedFile

        if not os.path.exists(self.getTargetDir()):
            print("{} does not exist".format(self.getTargetDir()))
            os.makedirs(self.getTargetDir())
        targetPath = self.getTargetDir() + os.sep + self.getTargetFile()
        self.crawler.linkTo(origPath, targetPath)

    def updateList(self):
        self.crawler.update(self.getCrawl(), self.getExt())

    def changeCrawlDir(self, newpath):
        self.configuration.changeConfig("crawldir", newpath)

    def changeTargetDir(self, newpath):
        self.configuration.changeConfig("targetdir", newpath)

    def changeExtension(self, newext):
        self.configuration.changeConfig("extension", newext)

    def changeTarget(self, newtarg):
        self.configuration.changeConfig("targetfile", newtarg)

    def saveConfig(self):
        self.configuration.writeConfFile()

    # get functions
    def getFiltered(self):
        self.updateList()
        return self.crawler.getFiltered()

    def getCrawl(self):
        return self.configuration.getConfig("crawldir")

    def getExt(self):
        return self.configuration.getConfig("extension")

    def getTargetDir(self):
        return self.configuration.getConfig("targetdir")

    def getTargetFile(self):
        return self.configuration.getConfig("targetfile")

    def getTargetPath(self):
        return self.configuration.getConfig("targetdir") + self.sep + self.configuration.getConfig("targetfile")


if __name__ == '__main__':
    print("Testing the UI Interaction functions")
    control = Controller()
    control.configuration.initialSetup()
    print(control.getFiltered())
    filtered = control.getFiltered()
    control.linkFile(filtered[0][0])
