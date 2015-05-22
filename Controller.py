import Indexer
import Configuration
import os

# the controller implements the configuration on the indexer operations, all
# user interface commands pass through the controller


class Controller:
    def __init__(self):
        # initialize the Controller object, first we would need to initialize
        # the configuration system
        # the configuration is saved in the appdata system
        self.configuration = Configuration.Configuration()
        self.crawler = Indexer.FileCrawler(self.configuration.getConfig("crawldir"),
                                           self.configuration.getConfig("extension"))

    def linkFile(self, selectedFile):
        origPath = self.configuration.getConfig("crawldir") + \
            os.sep + selectedFile
        targetPath = self.configuration.getConfig("targetdir") + os.sep + self.configuration.getConfig("targetfile")
        self.crawler.linkTo(origPath, targetPath)

    def updateList(self):
        self.crawler.update()

    def changeCrawlDir(self, newpath):
        self.configuration.changeConfig("crawldir", newpath)

    def changeTargetDir(self, newpath):
        self.configuration.changeConfig("targetdir", newpath)

    def changeExtension(self, newext):
        self.configuration.changeConfig("extension", newext)

    def changeTarget(self, newtarg):
        self.configuration.changeConfig("targetfile", newext)

if __name__ == '__main__':
    print("Testing the UI Interaction functions")
