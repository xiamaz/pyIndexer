import os
import re
import shutil


class FileCrawler:
    def __init__(self):
        pass

    def update(self, path, fileFormat):
        self.getFiles(path)
        self.filterFiles(path, fileFormat)

    def getFiles(self, path):
        self.files = os.listdir(path)

    def filterFiles(self, path, fileFormat):
        self.filtered = []
        expr = re.compile("\\{}$".format(fileFormat))
        for f in self.files:
            if expr.search(f):
                t = (f, os.path.getmtime(path + os.sep + f))
                self.filtered.append(t)

    def getFiltered(self):
        return self.filtered

    def linkTo(self, orig, new):
        shutil.copy(orig, new)

if __name__ == "__main__":
    pass
