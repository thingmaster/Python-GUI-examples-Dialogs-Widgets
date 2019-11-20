# Copyright @ 2018 Michael George
#
# some examples of putting simple controls on a main window, popup from a button click
# also pops up an About Box dialog
#
#   Python Compability:     Developed on IDLE@Python 3.7.1.
#   Platform Compatibilty:  recent testing on MacOS, Win10
#
#   mg 2018-12-21 initial upload to git
#
import tkinter as tk
from tkinter import Tk, OptionMenu, Label, Button, Checkbutton, Radiobutton, Scrollbar, Text, Entry, StringVar, BooleanVar, DISABLED, NORMAL, END, RIGHT, LEFT, W, IntVar, END, W, E, Y
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from MGAppInfo import mg_applicationinfo
from MGIniFiles import IniFileManager
from MGwidgets import MGradiogroup, MGcheckboxes

# basic aboutdialog exits on click of OK
# 
class AboutDialog:
    def __init__(self, parent):
        self.myparent = parent
        self.string1 = None

        # create the new toplevel window frame for this dialog
        # we been this window instance  'top' for creating widgets and quitting the dialog
        if parent:
            top = self.top = tk.Toplevel(parent)
        else:
            top = self.top = tk.Tk()
        #centerinwindow(top,700, 200)
        #top.configure(background='green')
        top.lift()
        appinf = mg_applicationinfo()
        self.myLabel = tk.Label(top, text='    '+
                                appinf.mg_getappname()+'  '+
                                appinf.mg_getappversion()+'    \n ',
                                font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.myLabel.grid(column=8, row=1, sticky=W+E)
        self.myLabel0 = tk.Label(top, text='    '+appinf.mg_getappcopyright())
                                #font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.myLabel0.grid(column=8, row=2, sticky=W+E)
        self.myLabel1 = tk.Label(top, text=' ',
                                font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.myLabel1.grid(column=9, row=3, sticky=W+E)
        self.myLabel2 = tk.Label(top, text=' ',
                                font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.myLabel2.grid(column=9, row=0, sticky=W+E)


        self.startbutton2text = StringVar()
        self.startbutton2text.set("OK")
        self.start_button2 = Button(top, textvariable=self.startbutton2text, command=self.onClick)
        #, font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.start_button2.grid(column=8, row=6 ) #, sticky=W+E)
        self.myLabel3 = tk.Label(top, text=' ',
                                font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.myLabel3.grid(column=9, row=7, sticky=W+E)
     #  dialog OK button click; closes the AboutDialog window
    def onClick(self):
        self.top.destroy() #Destroy()
        return

# optionsdialog for program setup options exits on click of OK
# note that the options are tied to INI file (IniFileContents class). 
#
class ProgramOptionsDialog:
    def __init__(self, parent, inifileinstance,varslist):
        self.myparent = parent
        self.string1 = None
        self.iniinfo = inifileinstance
        self.varslist = varslist

        print('iniinfo',self.iniinfo)
        # create the new toplevel window frame for this dialog
        # we been this window instance  'top' for creating widgets and quitting the dialog
        if parent:
            top = self.top = tk.Toplevel(parent)
        else:
            top = self.top = tk.Tk()
        #centerinwindow(top,700, 200)
        #top.configure(background='green')
        top.lift()
        appinf = mg_applicationinfo()


        self.radios = MGradiogroup(self.top, self.varslist, self.flyoverenter)
        self.checkboxes = MGcheckboxes(self.top, self.varslist, self.flyoverenter)
        #self.myLabel = tk.Label(top, text='    '+
        #                       appinf.mg_getappname()+'  '+
        #                        appinf.mg_getappversion()+'Options    \n ',
        #                        font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        #self.myLabel.grid(column=8, row=1, sticky=W+E)
        #self.myLabel0 = tk.Label(top, text='    '+'INI File' )
                                #font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        #self.myLabel0.grid(column=8, row=2, sticky=W+E)
        #self.myLabel1 = tk.Label(top, text=' ',
        ##                        font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        #self.myLabel1.grid(column=9, row=3, sticky=W+E)
        #self.myLabel2 = tk.Label(top, text=' ',
        #                        font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        #self.myLabel2.grid(column=9, row=0, sticky=W+E)


        self.startbutton2text = StringVar()
        self.startbutton2text.set("OK")
        self.start_button2 = Button(top, textvariable=self.startbutton2text, command=self.onClick)
        #, font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.start_button2.grid(column=2, row=6)#, sticky=W+E)
        
        self.cancelbutton2text = StringVar()
        self.cancelbutton2text.set("Cancel")
        self.cancel_button2 = Button(top, textvariable=self.cancelbutton2text, command=self.cancelClick)
        #, font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.cancel_button2.grid(column=4, row=6)#, sticky=W+E)


        self.applybutton2text = StringVar()
        self.applybutton2text.set("Apply")
        self.apply_button2 = Button(top, textvariable=self.applybutton2text, command=self.applyClick)
        #, font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.apply_button2.grid(column=4, row=6)#, sticky=W+E)

        str0 = self.iniinfo.iniitems['Options-IniPath'][2]
        self.myLabel3 = tk.Label(top, text=str0,
                                font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*')
        self.myLabel3.grid(column=1, row=7, sticky=W+E)

    #  dialog OK button click; closes the AboutDialog window
    def onClick(self):
        #test for any ini file changes and ask are you sure?
        self.top.destroy() #Destroy()
        return
    def cancelClick(self):
        self.top.destroy() #Destroy()
        return

    def applyClick(self):
        self.iniinfo.iniitems['Options-IniPath'][2].append('another1')
        self.iniinfo.MGU_writeinistuff()
        print('apply CLICKED')
        # update INI if changes()
        return
    def flyoverenter(self,msg):
        print("flyover",msg)
        
# test dialog example
class MyDialog:
    def __init__(self, parent):
        self.myparent = parent
        self.string1 = None
        top = self.top = tk.Toplevel(parent)
        self.myLabel = tk.Label(top, text='Enter your username below')
        self.myLabel.pack()

        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()

        #self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        #self.mySubmitButton.pack()

        self.startbutton2text = StringVar()
        self.startbutton2text.set("Scan secondary tgt")
        self.start_button2 = Button(top, textvariable=self.startbutton2text, command=lambda: self.update("start2")).pack()

        self.startbutton3text = StringVar()
        self.startbutton3text.set("askFolder")
        self.start_button3 = Button(top, textvariable=self.startbutton3text, command=lambda: self.update("askfolder")).pack()

        self.start_button4 = Button(top, text="AskFile", command=lambda: self.update("askfile")).pack()

        self.buttonok = Button(top, text="ok", command=lambda: self.onok()).pack()
        self.buttoncancel= Button(top, text="cancel", command=lambda: self.oncancel()).pack()

    def update(self,msg):
        if msg=='askfolder':
            newstr = filedialog.askdirectory() #self.browsefilebuttonservice()
            print(newstr)
        elif msg=='askfile':
            newstr = self.browsefilebuttonservice()
            print(newstr)
        else:
            print(msg)
        
    def send(self):
        #global username
        #username = self.myEntryBox.get()
        self.string1 = self.myEntryBox.get()

    # closed MyDialog window
    def oncancel(self):
        self.top.destroy()
        
    def onok(self):
        self.string1 = self.myEntryBox.get()
        self.top.destroy()
        return 

    def browsefilebuttonservice(self):
        file_opt = options =  {}
        #MAC fails  options['filetypes'] = [('gzipped SOFT', '.soft.gz'), ('SOFT', '.soft'),('Comma Separated', '.csv')]
        options['parent'] = self.myparent
        options['initialdir'] = 'data'
        options['title'] = "AHREA - Select data file."
        fname = askopenfilename(**options)
        #filetypes=[("JPG","*.jpg;*.jpeg"),
#                                           ("Docs","*.pdf;*.doc;*.docx;*.xls;*.xlsx"),
#                                           ("HTML files", "*.html;*.htm"),
#                                           ("All files", ".*")])
        if fname:
            try:
                print("Selected file: (%s)"%fname)
                return fname
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

#  dialog 
class MyReloadPreviousDBDialog:
    def __init__(self, parent, label1str):
        self.myparent = parent
        self.string1 = None
        top = self.top = tk.Toplevel(parent)
        self.myLabel = tk.Label(top, text=label1str)
        self.myLabel.pack()

        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()

        #self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        #self.mySubmitButton.pack()

        self.startbutton2text = StringVar()
        self.startbutton2text.set("Scan secondary tgt")
        self.start_button2 = Button(top, textvariable=self.startbutton2text, command=lambda: self.update("start2")).pack()

        self.startbutton3text = StringVar()
        self.startbutton3text.set("askFolder")
        self.start_button3 = Button(top, textvariable=self.startbutton3text, command=lambda: self.update("askfolder")).pack()

        self.start_button4 = Button(top, text="AskFile", command=lambda: self.update("askfile")).pack()

        self.buttonok = Button(top, text="ok", command=lambda: self.onok()).pack()
        self.buttoncancel= Button(top, text="cancel", command=lambda: self.oncancel()).pack()

    def update(self,msg):
        if msg=='askfolder':
            newstr = filedialog.askdirectory() #self.browsefilebuttonservice()
            print(newstr)
        elif msg=='askfile':
            newstr = self.browsefilebuttonservice()
            print(newstr)
        else:
            print(msg)
        
    def send(self):
        #global username
        #username = self.myEntryBox.get()
        self.string1 = self.myEntryBox.get()

    # closed MyDialog window
    def oncancel(self):
        self.top.destroy()
        
    def onok(self):
        self.string1 = self.myEntryBox.get()
        self.top.destroy()
        return 

    def browsefilebuttonservice(self):
        file_opt = options =  {}
        #MAC fails  options['filetypes'] = [('gzipped SOFT', '.soft.gz'), ('SOFT', '.soft'),('Comma Separated', '.csv')]
        options['parent'] = self.myparent
        options['initialdir'] = 'data'
        options['title'] = "AHREA - Select data file."
        fname = askopenfilename(**options)
        #filetypes=[("JPG","*.jpg;*.jpeg"),
#                                           ("Docs","*.pdf;*.doc;*.docx;*.xls;*.xlsx"),
#                                           ("HTML files", "*.html;*.htm"),
#                                           ("All files", ".*")])
        if fname:
            try:
                print("Selected file: (%s)"%fname)
                return fname
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return
# helper function to center and size a window
def centerinwindow(mywindow, wid, ht):
    # do some window size and placement math
    w = wid #400 # width for the Tk root
    h = ht #350 # height for the Tk root
    # get screen width and height
    ws = mywindow.winfo_screenwidth() # width of the screen
    hs = mywindow.winfo_screenheight() # height of the screen
    # calculate x and y dimensions for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    # set the dimensions of the window and set xy placement
    mywindow.geometry('%dx%d+%d+%d' % (w, h, x, y))



if __name__ == '__main__':
    def callbackfunc(msg):
        print(msg)

    print('|============\n|   Dialogs testing demo program. \n|   Version 0.0 January-2019\n|   *******\n|============\n')
    # click handler for the main window 'Click me' button events
    # 
    def onClick(rootwin):
        inputDialog = MyDialog(rootwin)
        rootwin.wait_window(inputDialog.top)
        print('Username: ', inputDialog.string1)


    #
    # click handler for the main window 'Click me' button events
    # closes the main / root window
    # 
    def onClickCancel(rootwin):
        rootwin.destroy()

    # construct a window with some controls and some actions with popup 
    root = tk.Tk()
    centerinwindow(root, 400,350)
    # put the two controls on the main window
    mainLabel = tk.Label(root, text='Example for pop up input box')
    mainLabel.pack()
    mainButton = tk.Button(root, text='Click me', command=lambda: onClick(root))
    mainButton.pack()
    mainButton = tk.Button(root, text='Cancel', command=lambda: onClickCancel(root))
    mainButton.pack()

    # after that is drawn, put up a modal AboutDialog
    adialog = AboutDialog(root)
    root.wait_window(adialog.top)

    iniitems = dict()
    iniitems['Dirs-DirsBlacklist'] = [ 'Dirs', 'DirsBlackList', ['pp4', 'system', 'grayson', 'test2']]
    iniitems['Dirs-DirsWhitelist'] = [ 'Dirs', 'DirsWhiteList', ['wwindows', 'wsystem', 'test1', 'test2']]
    iniitems['Dirs-DirsOtherMGlist'] = [ 'Dirs', 'DirsOtherMGList', ['mg001', 'system', 'test1', 'test2']]
    iniitems['Options-IniOpenRecent'] = [ 'Options','IniOpenRecent', ['xxwindows', 'system', 'test1', 'test2']]
    iniitems['Options-OtherMGOption'] = [ 'Options','OtherMGOption', ['yywindows', 'system', 'test1', 'test2']]
    iniitems['Options-IniPath'] = [ 'Options','IniPath', ['zzwindows', 'system', 'test1', 'test2']]
    iniinfo = IniFileManager(iniitems)      # instantiate the INI info

    menucallbacks = { "newfilefn":callbackfunc, "openfilefn":callbackfunc,
                       "printmenufn":callbackfunc, "helpmenufn":callbackfunc,
                       "aboutmenufn":callbackfunc,"optionmenufn":callbackfunc, "quitmenufn":callbackfunc,
                               "dumpoptsfn":callbackfunc,  "dumppath1menufn":callbackfunc }
    menustatevars = {'DumpOptions':IntVar(), 'HintsFlag':BooleanVar(), 'DeleteCheck':BooleanVar(), 'DupCheck':BooleanVar(),
                              'CopyCheck':BooleanVar(),
                              'PrintCheck':BooleanVar(), 'TimerCheck':BooleanVar(),'DBOptions':IntVar(), 'CsvOrLive':IntVar()}

    podialog= ProgramOptionsDialog(root,iniinfo,menustatevars)
    root.wait_window(podialog.top)

    root.mainloop()
