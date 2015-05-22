import os
import re
import shutil


class FileCrawler:
    def __init__(self, searchPath, fileEnding):
        self.path = searchPath
        self.expr = re.compile("\\{}$".format(fileEnding))

    def update(self):
        self.getFiles()
        self.filterFiles()

    def getFiles(self):
        self.files = os.listdir(self.home)

    def filterFiles(self):
        self.filtered = []
        for f in self.files:
            if self.expr.search(f):
                self.filtered.append(f)

    def getFiltered(self):
        return self.filtered

    def linkTo(self, orig, new):
        shutil.copy(orig, new)

if __name__ == "__main__":
    pass
