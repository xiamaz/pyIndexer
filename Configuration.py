# configuration class containing the values for crawl directory, target
# directory. File ending to be searched and target file name
import os


class Configuration:
    def __init__(self, appname='FixLinker'):
        self.FILE = "pyIndexer.conf"
        self.HOME = os.path.expanduser("~")
        self.APPDATA = os.getenv('APPDATA')
        self.conf = {}
        self.path = self.APPDATA + os.sep + appname
        if not os.path.exists(self.path + os.sep + self.FILE):
            os.makedirs(self.path)
            self.initialSetup()
            self.writeConfFile()
        else:
            self.readConfFile()

    def addConfig(self, name, value, default):
        self.conf[name] = value
        self.defaultConf[name] = default

    def getConfig(self, key):
        return self.conf[key]

    def changeConfig(self, key, newValue):
        if key in self.conf.keys():
            self.conf[key] = newValue

    def parseConfig(self):
        confText = ""
        for key in self.conf.keys():
            confText += "{}:".format(key)
            confText += "{}:".format(self.conf[key])
            confText += "{}\r\n".format(self.defaultConf[key])
        return confText

    def addConfLine(self, confLine):
        # read by lines from configuration file
        # 0 - config name; 1 - current value; 2 - default value
        cStrs = confLine.split(":", 2)
        self.addConfig(cStrs[0], cStrs[1], cStrs[2])

    def writeConfFile(self):
        confText = self.parseConfig()
        with open(self.path + os.sep + self.FILE) as cFile:
            cFile.write(confText)

    def readConfFile(self):
        with open(self.path + os.sep + self.FILE) as cFile:
            for cLines in cFile:
                self.addConfLine(cLines)

    def initialSetup(self):
        # these are the default settings
        # the default crawl directory is the user home folder
        home = os.path.expanduser("~")
        self.configuration.addConfig("crawldir", home, home)
        # the default target direcotry is the desktop dir under
        target = home + os.sep + 'Desktop' + os.sep + 'ups fold'
        self.configuration.addConfig("targetdir", target, target)
        # the default file ending is .neworders
        self.configuration.addConfig("extension", ".neworders", ".neworders")
        # the default target is upslink.csv
        targetfile = "upsship.csv"
        self.configuration.addConfig("targetfile", targetfile, targetfile)
