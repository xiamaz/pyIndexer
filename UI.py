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
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.view.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.view.xview)
        self.view.configure(yscroll=ysb.set, xscroll=xsb.set)

        style = ttk.Style()

        self.linkButton = ttk.Button(self, text="Create UPSLink",
                                     command=self.parent.linkFile)
        #  self.updateButton = ttk.Button(self, text="Refresh view",
                                     #  command=self.getList)

        self.view.grid(row=0, column=0, sticky="nswe")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="we")
        self.linkButton.grid(row=2, column=0, columnspan=2,
                             rowspan=1, sticky="nswe")

        self.columnconfigure(0, weight=8)
        self.rowconfigure(0, weight=8)
        self.rowconfigure(2, weight=1)
       #   self.updateButton.pack(side="bottom", fill="x")

    def getList(self):
        self.view.delete(*self.view.get_children())
        rlist = self.parent.getFiles()
        self.flist = []
        for f in rlist:
            # each tuple contains name and modification date of file
            f.append(self.view.insert('', 'end', text=f[0], values=(f[1],)))
            self.flist.append(f)

        self.parent.status.showLog("Relevant files loaded")

    def sortItems(self, col='modified', reverse=True):
        # l = [(time.mktime(time.strptime(self.view.set(v, col))),
        #       v) for v in self.view.get_children('')]

        self.flist.sort(reverse=reverse, key=lambda x: x[2])
        for index, f in enumerate(self.flist):
            self.view.move(f[3], '', index)

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

        self.heading('#0', text='Update view', command=self.parent.getList)

        self.heading('modified', text='Last modified',
                     command=self.parent.sortItems)

        self.pack(side="top", fill="both", expand=True)


class ControlView(tk.Toplevel):
    # create configurations dialog with following layout
    # bottom are cancel and confirm buttons
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.resizable(0,0)
        self.wm_title("UPS Linker Settings")
        self.focus_set()

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
        self.extLabel = ttk.Label(self.top, text="File Extension")
        self.targLabel = ttk.Label(self.top, text="Target File Name")

        # pack the small widgets in grid in top frame
        self.cdirButton.grid(column=0, row=0, sticky="we")
        self.tdirButton.grid(column=0, row=1, sticky="we")
        self.cdirLabel.grid(column=1, row=0, sticky="we")
        self.tdirLabel.grid(column=1, row=1, sticky="we")
        self.extLabel.grid(column=0, row=2, sticky="we", pady=5)
        self.targLabel.grid(column=0, row=3, sticky="we")
        self.extEdit.grid(column=1, row=2, sticky="we")
        self.targEdit.grid(column=1, row=3, sticky="we")

        self.cancelButton.pack(side="left")
        self.confirmButton.pack(side="right")

        # pack the big frames into the window
        self.top.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.bottom.pack(side="bottom", fill="x", expand=True, padx=10, pady=10)

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
        self.parent.getFiles()
        self.destroy()

    def cancel(self):
        self.destroy()


class StatusBar(ttk.Frame):
    def __init__(self, parent, * args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.message = tk.StringVar()

        style = ttk.Style()
        style.configure("Black.TLabel", foreground="black")
        style.configure("Green.TLabel", foreground="green")
        style.configure("Red.TLabel", foreground="red")

        self.statuslabel = ttk.Label(self, textvariable=self.message)
        self.showLog("Welcome to the file linker.")

        self.statuslabel.pack(side="left", fill="x", pady=5, padx=5)

        # statusbar showing output from last operation
        # colored for green - all fine, red - error, black - normal status
    def showLog(self, text):
        self.message.set(text)
        self.statuslabel.configure(style="Black.TLabel")

    def showSuccess(self, text):
        self.message.set(text)
        self.statuslabel.configure(style="Green.TLabel")

    def showFailure(self, text):
        self.message.set(text)
        self.statuslabel.configure(style="Red.TLabel")


class MenuBar(tk.Menu):
    def __init__(self, parent, * args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.add_command(label='Configuration', command=self.activateConfig)
        #self.add_command(label='Quit', command=self.quitWindow)

    def activateConfig(self):
        ControlView(self.parent)

    def quitWindow(self):
        self.parent.quit()


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ttk.Style()
        style.configure("Statusbar.TFrame", relief="groove")

        self.output = OutputView(self)
        self.status = StatusBar(self, style="Statusbar.TFrame")

        self.status.pack(side="bottom", fill="x")
        self.output.pack(side="left", fill="both", expand=True)

        # add object to control the mechanic

        self.controller = Controller.Controller()
        status = self.controller.startConf()
        print(status)
        if status == 1:
            print("Asking for directory")
            crawlpath = tkfile.askdirectory()
            self.controller.initConf(crawlpath)

        # load initial file data
        self.output.getList()

    # controller functions
    def getFiles(self):
        try:
            return self.controller.getFiltered()
        except FileNotFoundError:
            print("Filepath not existant")
            path = tkfile.askdirectory()
            self.controller.initConf(path)
            return self.getFiles()

    def linkFile(self):
        selection = self.output.getSelected()
        if selection == "":
            self.status.showFailure("Please select a file to link")
            return
        self.controller.linkFile(selection)
        self.status.showSuccess("File linked successfully")


def main():
    root = MainWindow()
    root.minsize(600, 400)
    root.wm_title("UPS Linker")
    root.iconbitmap("link_icon.ico")
    root.configure(background='white')
    menubar = MenuBar(root)
    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()
