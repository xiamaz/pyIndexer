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
        self.CONFVERSION = "1.1"
        self.conf = {}
        self.defaultConf = {}

    def startConf(self):
        if not os.path.exists(self.APPDATA):
            os.makedirs(self.APPDATA)
        if not os.path.exists(self.APPDATA + os.sep + self.FILE):
            print("Configuration file does not exist")
            return 1
            # self.initialSetup()
            # self.writeConfFile()
        status = self.readConfFile()
        return status

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

        return 0

    def writeConfFile(self):
        confText = self.parseConfig()
        versionText = "version;{}\r\n".format(self.CONFVERSION)
        with open(self.APPDATA + os.sep + self.FILE, 'w') as cFile:
            cFile.write(versionText + confText)

    def readConfFile(self):
        print("Start reading configuration file")
        with open(self.APPDATA + os.sep + self.FILE, 'r') as cFile:
            for i, cLines in enumerate(cFile):
                if i == 0:
                    print(cLines)
                    if "version" not in cLines:
                        print("No version statement in file")
                        oldConfig = 1
                        break
                    else:
                        vStr = cLines.split(";", 1)
                        print(vStr)
                        if vStr[1].strip() != self.CONFVERSION:
                            print("Old conf version")
                            oldConfig = 1
                            break
                        else:
                            print("Conf file version ok")
                            oldConfig = 0
                self.addConfLine(cLines)

        if oldConfig:
            os.remove(self.APPDATA + os.sep + self.FILE)
            return 1
        else:
            return 0

    def initialSetup(self, crawl):
        # these are the default settings
        # the default crawl directory is the user home folder
        home = os.path.expanduser("~")
        # crawl = home + os.sep + 'Testing'
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
