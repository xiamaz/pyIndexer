import tkinter as tk
import Controller


class OutputView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.searchbar = tk.Entry(self)
        self.text = tk.Text(self)

        self.searchbar.pack(side="top", fill="x")
        self.text.pack(side="bottom", fill="both", expand=True)
        # add a search bar and a list for found files


class ControlView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.oldlabel = tk.Label(self, text="Old file extension")
        self.newlabel = tk.Label(self, text="New file extension")
        self.oldentry = tk.Entry(self)
        self.newentry = tk.Entry(self)

        self.changebutton = tk.Button(self, text="Change file extensions",
                                      command=self.parent.changeFiles)

        self.showlabel = tk.LabelFrame(self, text="Output options")
        self.checkold = tk.Checkbutton(self.showlabel, text="old extensioN")
        self.checknew = tk.Checkbutton(self.showlabel, text="new extension")
        self.checkall = tk.Checkbutton(self.showlabel, text="show all")
        self.updatebutton = tk.Button(self.showlabel, text="Update view")

        # set layout using grid layout to realize multiple rows of controls
        self.oldlabel.grid(row=0)
        self.oldentry.grid(row=1)
        self.newlabel.grid(row=2)
        self.newentry.grid(row=3)
        self.changebutton.grid(row=4)

        self.showlabel.grid(row=5)

        self.checkold.pack(anchor="e", fill="x")
        self.checknew.pack(anchor="e", fill="x")
        self.checkall.pack(anchor="e", fill="x")
        self.updatebutton.pack(anchor="e", fill="x")

        # double entry field for old and new extension name
        # button to do changes
        # button to show files with missing new extensions


class StatusBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.statuslabel = tk.Label(self, text="Generic output")

        self.statuslabel.pack(side="left", fill="x")

        # statusbar showing output from last operation
        # colored for green - all fine, red - error, black - normal status


class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.output = OutputView(self)
        self.control = ControlView(self)
        self.status = StatusBar(self, borderwidth=1, relief="sunken")

        self.status.pack(side="bottom", fill="x")
        self.control.pack(side="right", fill="y", anchor="center", expand=True)
        self.output.pack(side="left", fill="both", expand=True)

        self.controller = Controller.Controller()

    def updateView(self):
        pass

    def changeClick(self):
        pass

    def exprChange(self):
        pass

    def searchChange(self):
        pass


def main():
    root = tk.Tk()
    MainWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()
