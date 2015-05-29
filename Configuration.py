# configuration class containing the values for crawl directory, target
# directory. File ending to be searched and target file name
import os
import appdirs


class Configuration:
    def __init__(self, appname='UPSLinker', appauthor='Alcasa'):
        self.FILE = "pyIndexer.conf"
        self.HOME = os.path.expanduser("~")
        self.APPDATA = appdirs.user_data_dir(appname, appauthor)
        self.SEPERATOR = ";"
        self.conf = {}
        self.defaultConf = {}
        if not os.path.exists(self.APPDATA):
            os.makedirs(self.APPDATA)
        if not os.path.exists(self.APPDATA + os.sep + self.FILE):
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
            confText += "{0}{1}".format(key.strip(), self.SEPERATOR)
            confText += "{0}{1}".format(self.conf[key].strip(), self.SEPERATOR)
            confText += "{}\r\n".format(self.defaultConf[key].strip())
        return confText

    def addConfLine(self, confLine):
        # read by lines from configuration file
        # 0 - config name; 1 - current value; 2 - default value
        cStrs = confLine.split(self.SEPERATOR, 2)
        if len(cStrs) == 3:
            self.addConfig(cStrs[0], cStrs[1], cStrs[2])
        else:
            print("Invalid config line, ignore data")

    def writeConfFile(self):
        confText = self.parseConfig()
        with open(self.APPDATA + os.sep + self.FILE, 'w') as cFile:
            cFile.write(confText)

    def readConfFile(self):
        with open(self.APPDATA + os.sep + self.FILE, 'r') as cFile:
            for cLines in cFile:
                self.addConfLine(cLines)

    def initialSetup(self):
        # these are the default settings
        # the default crawl directory is the user home folder
        home = os.path.expanduser("~")
        crawl = home + os.sep + 'Testing'
        self.addConfig("crawldir", crawl, crawl)
        # the default target direcotry is the desktop dir under
        target = home + os.sep + 'Desktop' + os.sep + 'ups fold'
        self.addConfig("targetdir", target, target)
        # the default file ending is .neworders
        self.addConfig("extension", ".neworders", ".neworders")
        # the default target is upslink.csv
        targetfile = "upsship.csv"
        self.addConfig("targetfile", targetfile, targetfile)


if __name__ == '__main__':
    print("Testing the configurator")
    conf = Configuration()
    print(conf.APPDATA)
