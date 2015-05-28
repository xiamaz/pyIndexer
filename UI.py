import tkinter as tk
import tkinter.filedialog as tkfile
from tkinter import ttk
import Controller
import time


class OutputView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.view = ViewTable(self)
        self.linkButton = ttk.Button(self, text="Create UPSLink",
                                     command=self.parent.linkFile)
        self.updateButton = ttk.Button(self, text="Refresh view",
                                       command=self.getList)

        self.view.pack(side="top", fill="both", expand=True)
        self.linkButton.pack(side="bottom", fill="x", expand=True)
        self.updateButton.pack(side="bottom", fill="x", expand=True)

    def getList(self):
        self.view.delete(*self.view.get_children())
        flist = self.parent.getFiles()
        for f in flist:
            # each tuple contains name and modification date of file
            print(f[1])
            self.view.insert('', 'end', text=f[0], values=(f[1],))

        self.parent.status.showLog("Relevant files loaded")

    def sortItems(self, col='modified', reverse=True):
        l = [(time.mktime(time.strptime(self.view.set(v, col))),
              v) for v in self.view.get_children('')]
        l.sort(reverse=reverse)
        print(l)
        for index, (val, v) in enumerate(l):
            self.view.move(v, '', index)

        self.view.heading(col, command=lambda:
                          self.sortItems(col, not reverse))
        self.parent.status.showLog("List sorted by date")

    def getSelected(self):
        text = self.view.item(self.view.selection(), 'text')
        return text


class ViewTable(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, columns=('modified'), selectmode="browse",
                         *args, **kwargs)
        self.parent = parent

        self.column('modified')

        self.heading('modified', text='Last modified',
                     command=self.parent.sortItems)

        self.pack(side="top", fill="both", expand=True)


class ControlView(tk.Toplevel):
    # create configurations dialog with following layout
    # bottom are cancel and confirm buttons
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # variables
        self.cdir = tk.StringVar(self, self.parent.controller.getCrawl())
        self.tdir = tk.StringVar(self, self.parent.controller.getTargetDir())
        self.ext = tk.StringVar(self, self.parent.controller.getExt())
        self.tfile = tk.StringVar(self, self.parent.controller.getTargetFile())

        self.bottom = ttk.Frame(self)
        self.top = ttk.Frame(self)

        self.cancelButton = ttk.Button(self.bottom, text="Cancel",
                                       command=self.cancel)
        self.confirmButton = ttk.Button(self.bottom, text="Confirm",
                                        command=self.confirm)

        self.cdirButton = ttk.Button(self.top, text="Change Crawl Directory",
                                     command=self.changeCrawl)
        self.tdirButton = ttk.Button(self.top, text="Change Target Direcotry",
                                     command=self.changeTarget)

        self.cdirLabel = ttk.Label(self.top, textvariable=self.cdir)
        self.tdirLabel = ttk.Label(self.top, textvariable=self.tdir)

        self.extEdit = ttk.Entry(self.top, textvariable=self.ext)
        self.targEdit = ttk.Entry(self.top, textvariable=self.tfile)

        # pack the small widgets in grid in top frame
        self.cdirButton.grid(column=0, row=0)
        self.tdirButton.grid(column=0, row=1)
        self.cdirLabel.grid(column=1, row=0)
        self.tdirLabel.grid(column=1, row=1)
        self.extEdit.grid(column=0, row=2, columnspan=2)
        self.targEdit.grid(column=0, row=3, columnspan=2)

        self.cancelButton.pack(side="left")
        self.confirmButton.pack(side="left")

        # pack the big frames into the window
        self.top.pack(side="left", fill="both", expand=True)
        self.bottom.pack(side="bottom", fill="x", expand=True)

    def changeCrawl(self):
        self.cdir.set(tkfile.askdirectory(initialdir=self.cdir.get()))

    def changeTarget(self):
        self.tdir.set(tkfile.askdirectory(initialdir=self.cdir.get()))

    def confirm(self):
        self.parent.controller.changeCrawlDir(self.cdir.get())
        self.parent.controller.changeTargetDir(self.tdir.get())
        self.parent.controller.changeExtension(self.extEdit.get())
        self.parent.controller.changeTarget(self.targEdit.get())
        self.parent.controller.saveConfig()
        self.destroy()

    def cancel(self):
        self.destroy()


class StatusBar(ttk.Frame):
    def __init__(self, parent, * args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.showLog("Welcome to the file linker.")

        self.statuslabel = ttk.Label(self, text=self.message)

        self.statuslabel.pack(side="left", fill="x")

        # statusbar showing output from last operation
        # colored for green - all fine, red - error, black - normal status
    def showLog(self, text):
        self.message = text
        self.color = "black"

    def showSuccess(self, text):
        self.message = text
        self.color = "green"

    def showFailure(self, text):
        self.message = text
        self.color = "red"


class MenuBar(tk.Menu):
    def __init__(self, parent, * args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.add_command(label='Configuration', command=self.activateConfig)
        self.add_command(label='Quit', command=self.quitWindow)

    def activateConfig(self):
        ControlView(self.parent)

    def quitWindow(self):
        self.parent.quit()


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.output = OutputView(self)
        self.status = StatusBar(self)

        self.status.pack(side="bottom", fill="x")
        self.output.pack(side="left", fill="both", expand=True)

        # add object to control the mechanic
        self.controller = Controller.Controller()

        # load initial file data
        self.output.getList()

    # controller functions
    def getFiles(self):
        return self.controller.getFiltered()

    def linkFile(self):
        selection = self.output.getSelected()
        print(selection)
        self.controller.linkFile(selection)
        self.status.showSuccess("File linked successfully")


def main():
    root = MainWindow()
    root.minsize(600, 400)
    root.configure(background='white')
    menubar = MenuBar(root)
    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()
