import tkinter as tk
import tkinter.filedialog as tkfile
from tkinter import ttk
import Controller


class OutputView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.view = ViewTable(self)
        self.linkButton = tk.Button(self, text="Click!")

        self.view.pack(side="top", fill="both", expand=True)
        self.linkButton.pack(side="bottom", fill="x", expand=True)

    def getList(self):
        pass

    def sortItems(self):
        pass

    def getSelected(self):
        return self.view.selection()[0]


class ViewTable(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(self, parent, columns=('modified'), *args, **kwargs)
        self.parent = parent

        self.heading('modified', text='Last modified')
        self.insert('', 'end', 'initial', text='initial ID')

        self.pack(side="top", fill="both", expand=True)


class ControlView(tk.Toplevel):
    # create configurations dialog with following layout
    # bottom are cancel and confirm buttons
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # variables
        self.cdir = tk.StringVar(self, "Dummy Text")
        self.tdir = tk.StringVar(self, "Dummy Text")

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

        self.extEdit = ttk.Entry(self.top)
        self.targEdit = ttk.Entry(self.top)

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
        self.cdir = tkfile.askdirectory()

    def changeTarget(self):
        self.tdir = tkfile.askdirectory()

    def confirm(self):
        self.parent.controller.changeCrawlDir(self.cdir)
        self.parent.controller.changeTargetDir(self.tdir)
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


class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.output = OutputView(self)
        self.status = StatusBar(self)

        self.status.pack(side="bottom", fill="x")
        self.output.pack(side="left", fill="both", expand=True)

        # add object to control the mechanic
        self.controller = Controller.Controller()

    # controller functions
    def getFiles(self):
        return self.controller.getFiltered()

    def linkFile(self):
        selection = self.output.getSelected().text()
        crawlpath = self.controller.getCrawl() + self.controller.sep + selection
        targetpath = self.controller.getTargetPath()
        self.controller.linkFile(crawlpath, targetpath)


def main():
    root = tk.Tk()
    root.minsize(600, 400)
    root.configure(background='white')
    MainWindow(root).pack(side="top", fill="both", expand=True)
    menubar = MenuBar(root)
    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()
