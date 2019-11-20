# 
# Copyright @ 2018, 2019 Michael George
#
# MGwidgets implements some basic widget classes for reuse: buttons, boxes, entry, menus
# revisions:
#    2018-12-06 mg initial version with main menu and a combo button with list of checkboxes
#    2018-12-20 add the file menu. add the help menu. 
#       remove local state vars from these widgets, use keyval pairs provided by caller to store menu & gui state values
#       added binding example for widgets Enter Leave & flyover callback argument in the class
#       extended the indirection via keyvaluestatevars to include the dynamic menu options that are added as new databases are scannned
#    2019-02-23 add the radioubutton to choose copying current tree of unique files to new target OR delete duplicates in current tree of files
#
from tkinter import Tk, OptionMenu, Label, Button, Menu, Menubutton, Checkbutton, Radiobutton, Scrollbar, Text, Entry, StringVar, BooleanVar
from tkinter import RAISED, DISABLED, NORMAL, END, RIGHT, LEFT, W, IntVar, BooleanVar, END, W, E, Y
from tkinter.messagebox import showerror
import sys

# MG Class for creating and managing a main menu bar with multiple command menus, check menus, radio menus
# caller must provide
#     the 'topwin' parent window handle and two keyvalue lists
#     the keyvalcallbacks dict with named callbacks for every menu function,
#     the keyvalstatevars dict with named variables for every variable menu state
class mgmainmenu:
    # init application menubar, the Dump Options menu and the Database Select options + another Info/help/about
    # the callbacks are in a dictionary like "newfilefn":MGU_newfilefn ...
    # the statevars are in a dictionary like "dumpfileopt":MGU_dumpfileoptval
    # caller provides them... menu state changes update them/ call them
    def __init__( self, topwin, keyvalcallbacks, keyvalstatevars ):
        self.parent = topwin
        self.menubar = Menu(self.parent)
        self.keyvalstatevars = keyvalstatevars
        #???self.view_menu = Menu(self.menubar)
        # the file menu
        Command_button = Menubutton(self.menubar, text='Simple Button Commands',  underline=0)
        Command_button.menu = Menu(Command_button)
        #Command_button.menu = Menu(self.menubar)
        Command_button.menu.add_command(label="Undo")
        # undo is the 0th entry...
        Command_button.menu.entryconfig(0, state=DISABLED)
        Command_button.menu.add_command(label='New...', underline=0, command=keyvalcallbacks["newfilefn"])
        Command_button.menu.add_command(label='Open...', underline=0, command=keyvalcallbacks["openfilefn"])
        Command_button.menu.add_command(label='ReScan...', underline=0, command=keyvalcallbacks["rescanmenufn"])
        # alternate font example
        Command_button.menu.add_command(label='Print', underline=0,
                                    font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*',
                                    command=keyvalcallbacks["printmenufn"])
        # separator example
        Command_button.menu.add('separator')
        Command_button.menu.add_command(label='Options', underline=0,
                                    font='-*-helvetica-*-r-*-*-*-180-*-*-*-*-*-*',
                                    command=keyvalcallbacks["optionmenufn"])

        # aLternate color example
        Command_button.menu.add_command(label='Quit', underline=0,
                                    background='red',
                                    activebackground='green',
                                    command=keyvalcallbacks["quitmenufn"])
        self.menubar.add_cascade(label='File', menu=Command_button.menu)

        #self.menubar.add_cascade(label='View', menu=self.view_menu)
        # add a menubar menu to select option for dumping all elements, or only Dups or only Unique
        self.dumpselect_menu = Menu(self.menubar)
        self.dumpradioval= IntVar()
        self.dumpradioval.set(1)
        self.dumpselect_menu.add_radiobutton(label="Dump All", value=1,variable=keyvalstatevars['DumpOptions'])
        self.dumpselect_menu.add_radiobutton(label="Dump only unique",value=2,variable=keyvalstatevars['DumpOptions'])
        self.dumpselect_menu.add_radiobutton(label="Dump only Dups",value=3,variable=keyvalstatevars['DumpOptions'])
        self.dumpselect_menu.add('separator')
        self.dumpselect_menu.add_command(label='Default header log path', underline=0,
                                    background='red',
                                    activebackground='green',
                                    command=keyvalcallbacks["dumppath1menufn"])
        self.menubar.add_cascade(label='Dump File options', menu=self.dumpselect_menu)

        self.dumpdbselect_menu1 = Menu(self.menubar)
        self.menubar.add_cascade(label='Dump DB selection', menu=self.dumpdbselect_menu1)
        # add a placeholder for this menu with zero databases added in memory
        # this DUMP DB menu will be dynamically extended as new databases are scanned.
        #  the parent owner of the class instance must call the add method of this class to extend the menu
        self.dumpdbselect_menu1.add_command(label="<None>")
        # <None> is the 0th entry...
        self.dumpdbselect_menu1.entryconfig(0, state=DISABLED)
        # set a flag just so we can delete this <None> placeholder during first menu add operation
        self.newmenu = True

        self.dumpvolselect_menu1 = Menu(self.menubar)
        self.menubar.add_cascade(label='Dump Volume selection', menu=self.dumpvolselect_menu1)
        # add a placeholder for this menu with zero databases added in memory
        # this DUMP DB menu will be dynamically extended as new databases are scanned.
        #  the parent owner of the class instance must call the add method of this class to extend the menu
        self.dumpvolselect_menu1.add_command(label="<None>")
        # <None> is the 0th entry...
        self.dumpvolselect_menu1.entryconfig(0, state=DISABLED)
        # set a flag just so we can delete this <None> placeholder during first menu add operation
        self.newvolmenu = True

        # menu begins with only one  option- dump all
        #self.dumpdbselect_menu1.add_checkbutton(label="<None>", onvalue=False, offvalue=False, variable=self.var01)#variable=self.show_all)

        #
        # add a menubar menu for the app info Help/ about/ etc
        self.show_all = IntVar()
        self.show_all.set(True)
        self.vendorhelp_menu = Menu(self.menubar)
        self.help001 = { "Help":self.show_all}
        # menu begins with only one  option- dump all
        self.vendorhelp_menu.add_checkbutton(label="Show _Hints", onvalue=True, offvalue=False, variable=keyvalstatevars['HintsFlag'])
        self.vendorhelp_menu.add_checkbutton(label="Monitor volumes (10second timer activity)", onvalue=True, offvalue=False, variable=keyvalstatevars['TimerCheck'])
        self.vendorhelp_menu.add_command(label='Help...', underline=0, command=keyvalcallbacks["helpmenufn"])
        # separator example
        self.vendorhelp_menu.add('separator')
        self.vendorhelp_menu.add_command(label='Dbg info dump...', underline=0, command=self.MGmenudumpdbg)
        self.vendorhelp_menu.add_checkbutton(label='Dbg runtime info@HIGH', onvalue=True, offvalue=False, variable=keyvalstatevars['DebuginfohighFlag'])
        self.vendorhelp_menu.add_command(label='About...', underline=0, command=keyvalcallbacks["aboutmenufn"])
        self.menubar.add_cascade(label='Help', menu=self.vendorhelp_menu)

        # register all this with the callers parent window frame
        self.parent.config(menu=self.menubar)

    # add a menuitem to the check options in the database selection menu list
    # this option allows the databases to be added as they are specified & scanned by user
    # later used as criteria for which source data to include in the dump of memory database
    # NOTE that the caller MUST extend the @keyvalstatevars[] list to include the newlabel Key-Value pair for this new item with an associated BooleanVar()
    #   and init the associated variable (I default to False i.e. unchecked)
    def mgmenuitem_adddb(self, newlabel, addseparator=False):
        # if this is the first database added, lets remove the <None> menu option!
        if self.newmenu:
            self.newmenu = False
            self.dumpdbselect_menu1.delete(0, END)
        self.dumpdbselect_menu1.add_checkbutton(label=newlabel, onvalue=True, offvalue=False, variable=self.keyvalstatevars[newlabel])
        if addseparator:
            self.dumpdbselect_menu1.add('separator')

    def mgmenuitem_addvol(self, newlabel, addseparator=False):
        # if this is the first database added, lets remove the <None> menu option!
        if self.newmenu:
            self.newmenu = False
            self.dumpdbselect_menu1.delete(0, END)
        self.dumpvolselect_menu1.add_checkbutton(label=newlabel, onvalue=True, offvalue=False, variable=self.keyvalstatevars[newlabel])
        if addseparator:
            self.dumpvolselect_menu1.add('separator')    # get the menu radio selection for including All/Unique/Duplicate files in the dump
    #def mgmenuselection_dumpoptions_get(self):
    #    return self.dumpradioval.get()  ALL OF THE MENU STATES SHOULD LIE IN PARENT OF THIS INSTANCE! see keyvalstatevars{}
    # def MGmenugroups_get(self):
    #   return self.mgmenuselection_dumpoptions_get(), self.keyvalstatevars.it

    # tutorial dump of the state of the menu vars dictionary
    def MGmenudumpdbg(self):
        for i, (k,v) in enumerate(self.keyvalstatevars.items()):
            print(i, k,  v.get())

#
# an MG Class for creating & interacting with a button that has check items
#  includes a _get function returning keyvalue pairs for all check items' states
#  includes an _add method adding the item you request (note if it's not unique you only get key-value info for 1st)
#
class mgcombocheckboxes:
    def __init__( self, topwin, itemkeyval):
        self.parentframe=topwin
        self.mb = Menubutton ( topwin, text="CheckComboBox", relief=RAISED )
        self.mb.grid()            
        self.mb.menu  =  Menu( self.mb, tearoff = 0 )
        self.mb["menu"] = self.mb.menu
        #
        #self.mb.menu["menu"] = self.mb.menu
        self.itemischecked = {}
        self.comboitemcount = 0
        for menuentry in itemkeyval:
            itemvar = IntVar()
            itemvar.set(itemkeyval[menuentry])
            # a keyvalue pair with menu item name and an itemvar unique to that selection
            self.itemischecked[menuentry] = itemvar
            self.mb.menu.add_checkbutton ( label=menuentry, variable=itemvar)
            self.comboitemcount += 1
        #self.mb.config(menu=self.mb.menu)
            
    def grid(self, row, column):
        #self.mb.grid(row=5, column=7)
        pass

    #return the KV pairs of the combobuttons true/false checked or not
    def mgcombochecks_get( self ):
        return self.itemischecked
    
    def mgcombochecks_add( self, itemstr ):
            itemvar = IntVar()
            itemvar.set(False)
            # a keyvalue pair with menu item name and an itemvar unique to that selection
            self.itemischecked[itemstr] = itemvar
            self.mb.menu.add_checkbutton ( label=itemstr, variable=itemvar)
            self.comboitemcount +=1 
# MG class for managing all the radio groups in a window
class MGradiogroup():
    # init the instance of MGradiogroup( parentwin, kvgrouppairs, flyover_entryfn)
    #  kvgrouppairs is the keyvalue pairs with variables that are associated with the radio options
    # example of full implementation in MGGuiUtils.py - see MGradiogroup instantiation
    #
    def __init__(self, parentwin, kvgrouppairs, flyoverfn):
        # CSV Generation options radio button
        self.master = parentwin
        self.kvgrouppairs = kvgrouppairs
        self.flyoverfn = flyoverfn

        # first radio group; note that command= callback is not needed. add it if you want to process clicks as they happen. my app just gets the state from vars
        Radiobutton(parentwin, text = "All Files", variable=kvgrouppairs['DumpOptions'],  value = 1).grid(row=2, column=4,sticky=W) #command=self.MGradiogroup_fn,
        Radiobutton(parentwin, text = "Exclude Dups", variable=kvgrouppairs['DumpOptions'], value=2).grid(row=2, column=5,sticky=W)#command=self.MGradiogroup_fn,
        Radiobutton(parentwin, text = "Only Dups", variable=kvgrouppairs['DumpOptions'],value=3).grid(row=2,column=6, sticky=W)#command=self.MGradiogroup_fn,
        # second radio grou- which databases to operate on
        Radiobutton(parentwin, text = "All DBs", variable=kvgrouppairs['DBOptions'], value=1).grid(row=4,column=4, sticky=W)
        Radiobutton(parentwin, text = "Only in selected DB", variable=kvgrouppairs['DBOptions'], value=2).grid(row=4,column=5, sticky=W)
        Radiobutton(parentwin, text = "Not in selected DB", variable=kvgrouppairs['DBOptions'], value=3).grid(row=4,column=6, sticky=W)
        # third radio group
        #init the db from file or folder  radio button)
        rb1 = Radiobutton(parentwin, text = "Load\nCSV", variable=self.kvgrouppairs['CsvOrLive'], value = 1) #command=self.inittypeFn, 
        rb1.grid(row=1, column=5,sticky=W)
        rb2 = Radiobutton(parentwin, text = "Scan\nTree", variable=self.kvgrouppairs['CsvOrLive'], value = 2) #, command=self.inittypeFn
        rb2.grid(row=1, column=6,sticky=W)
        rb1.bind("<Enter>",lambda event:self.flyoverfn("Choose LOAD CSV to load memory database from an existing .CSV file database (dumped from previous filesystem scan)\n"+
                                                               "This may be useful for checking a new filesystem against your existing set of files where:\n"+
                                                               "  a) you don't want to RE-scan your base files which may be huge list and take hours\n"+
                                                               "  b) you don't have direct access to the backup, or it is very slow network access"))
        rb1.bind("<Leave>",lambda event:self.flyoverfn(None))
        rb2.bind("<Enter>",lambda event:self.flyoverfn("Choose SCAN TREE to load memory database from a target filesystem in the current system\n\n\n"))
        rb2.bind("<Leave>",lambda event:self.flyoverfn(None))

        # fourth radio group choose to COPY Unique files to a destination or to DELETE dups from a source!
        #
        rb1 = Radiobutton(parentwin, text = "Copy unique files", variable=self.kvgrouppairs['DeleteInsteadofCopy'], value = False) #command=self.inittypeFn, 
        rb1.grid(row=3, column=5,sticky=W)
        rb2 = Radiobutton(parentwin, text = "Delete DUPs in source", variable=self.kvgrouppairs['DeleteInsteadofCopy'], value = True) #, command=self.inittypeFn
        rb2.grid(row=3, column=6,sticky=W)
        rb1.bind("<Enter>",lambda event:self.flyoverfn("Choose Choose COPY to write unique files to a new target folder (i.e. build a NEW, cleaner file tree)\n"+
                                                               "Choose DELETE to delete duplicate files in a current database (i.e. clean the current files tree\n"+
                                                               "  a) you don't want to RE-scan your base files which may be huge list and take hours\n"+
                                                               "  b) you don't have direct access to the backup, or it is very slow network access"))
        rb1.bind("<Leave>",lambda event:self.flyoverfn(None))
        rb2.bind("<Enter>",lambda event:self.flyoverfn("Choose DELETE to delete duplicate files in a current database (i.e. clean the current files tree\n\n\n"))
        rb2.bind("<Leave>",lambda event:self.flyoverfn(None))

    # anyone with the instance can get the state of the two radio groups. don't really need this either except for tutorial app.
    # in a real application, the instantiating caller provides these menu-associated variables so THEY RESIDE IN THE CALLER'S CONTEXT - caller can access directly
    def MGradiogroup_get(self):
        print("radiogroupget", self.kvgrouppairs['DumpOptions'].get(), self.kvgrouppairs['DBOptions'].get())
        return self.kvgrouppairs['DumpOptions'].get(), self.kvgrouppairs['DBOptions'].get()

    # callback on clicks to show the state of the two radio groups. don't really need this for app but it's a good tutorial helper 
    def MGradiogroup_fn(self):
        print("dumpopts", self.kvgrouppairs['DumpOptions'].get())
        print("dbopts", self.kvgrouppairs['DBOptions'].get())
        return

# mg class for managing all the checkboxes in a window
class MGcheckboxes():
    # init the instance of MGcheckboxes( parentwin, kvgrouppairs, flyover_entryfn)
    #  kvgrouppairs is the keyvalue pairs with variables that are associated with the checkbox options
    # example of full implementation in MGGuiUtils.py - see MGradiogroup instantiation
    #
    def __init__(self, parentwin, kvgrouppairs, flyoverfn, baserow=6):
        # CSV Generation options check button
        self.master = parentwin
        self.kvgrouppairs = kvgrouppairs
        self.flyoverfn = flyoverfn

        # the checkbox gui items to enable / disable various optional activities
        self.delbutton = Checkbutton(parentwin, text="Delete\nselected", variable=self.kvgrouppairs['DeleteCheck'], onvalue=True, offvalue=False).grid(row=baserow+15, column=4, columnspan=1, sticky=W)
        self.copycheckbutton = Checkbutton(parentwin, text="Copy\nselected", variable=self.kvgrouppairs['CopyCheck'], onvalue=True, offvalue=False).grid(row=baserow+15, column=3, columnspan=1, sticky=W)
        self.printcheckbutton = Checkbutton(parentwin, text="Print CSV recs", variable=self.kvgrouppairs['PrintCheck'], onvalue=True, offvalue=False).grid(row=baserow+15, column=2,columnspan=1, sticky=W)
        self.dupcheckbutton = Checkbutton(parentwin, text="Dup checking", variable=self.kvgrouppairs['DupCheck'], onvalue=True, offvalue=False).grid(row=baserow+15, column=1,columnspan=1, sticky=W)
        # note that we don't need to keep the handle to the check buttons so they are not instance self.xx variables
        timercheckbutton = Checkbutton(parentwin, text="Timer enable", variable=self.kvgrouppairs['TimerCheck'], onvalue=True, offvalue=False)
        timercheckbutton.grid(row=baserow+15, column=0,columnspan=1, sticky=W)
        timercheckbutton.bind("<Enter>",lambda event:self.flyoverfn("You can turn the timer off so that timer won't monitor insertion/removal automatically\n\n\n"))
        timercheckbutton.bind("<Leave>",self.flyoverfn(None))

    # anyone with the instance can get the state of the two radio groups. don't really need this either except for tutorial app.
    # in a real application, the instantiating caller provides these menu-associated variables so THEY RESIDE IN THE CALLER'S CONTEXT - caller can access directly
    def MGradio_get(self):
        return 

    # callback on clicks to show the state of the two radio groups. don't really need this for app but it's a good tutorial helper 
    def MGcheck_fn(self):
        return

  
if __name__ == '__main__':
    # init a root window var to reference in the quit button
    myroot = None
    def cbfunc():
        print("example callback fn")
    def quitfunc():
        print("quit")
        myroot.destroy()

    # display hints when mouse <Entry> events get us here
    # clear hints when <Leave> events get us here
    # the menu has a check item to turn the behavior on/ off
    def flyoverfunc(str):
        # no hints if the GUI / menu flag is not checked
        if not menustatevars['HintsFlag'].get():
            return
        if str:
            print("flyover",str)
        
    def Item_test(comboinstance,menuinstance):
        mychks= comboinstance.mgcombochecks_get()
        for myitem in mychks:
            print( myitem, "state=", mychks[myitem].get())
        menudata = menuinstance.mgmenuselections_dumpget()
        for mdbsel in menudata:
         print("menudbsel", mdbsel, menudata[mdbsel].get())
         #.show_all.get(),menuinstance.show_done.get())
        print("menudump",menuinstance.dumpradioval.get())
        # add more items to a menu
        menuinstance.mgmenuitem_add("another item:%1d"%menuinstance.dumpdbselectcount)
        # add more check items to the combo button
        comboinstance.mgcombochecks_add( "another button menu item:%1d"%comboinstance.comboitemcount)

    myroot = Tk()
    menucallbacks = { "newfilefn":cbfunc, "openfilefn":cbfunc,
            "printmenufn":cbfunc, "helpmenufn":cbfunc,
            "aboutmenufn":cbfunc, "quitmenufn":quitfunc,
            "dumpoptsfn":cbfunc }
    menustatevars = {'DumpOptions':IntVar(), 'HintsFlag':BooleanVar(), 'DeleteCheck':BooleanVar(), 'DupCheck':BooleanVar(),
                          'CopyCheck':BooleanVar(),
                          'PrintCheck':BooleanVar(), 'TimerCheck':BooleanVar(),'DBOptions':IntVar(), 'CsvOrLive':IntVar()}
    menustatevars['DumpOptions'].set(1)
    menustatevars['DBOptions'].set(1)
    menustatevars['DumpOptions'].set(1)
    menustatevars['HintsFlag'].set(False)
    menustatevars['DeleteCheck'].set(False)
    menustatevars['DupCheck'].set(False)
    menustatevars['CopyCheck'].set(False)
    menustatevars['PrintCheck'].set(True)
    menustatevars['TimerCheck'].set(True)
    menustatevars['CsvOrLive'].set(2)

    mgmenu = mgmainmenu(myroot,menucallbacks,menustatevars )
    mgcombo1 = mgcombocheckboxes( myroot, {'Item0':False,'Item1':False,'Item2':True,'Item3':True})
    mgcombo1.grid(6, 1)
    button1 = Button(myroot, text="Item True/False Test", command = lambda: Item_test(mgcombo1,mgmenu))
    button1.grid(row=5, column=6)

    #create the radio button group via class in MGwidgets.py
    radios = MGradiogroup(myroot, menustatevars, flyoverfunc)
    checks = MGcheckboxes(myroot, menustatevars, flyoverfunc)
    

    myroot.title( "MGwidgets-3.8-002-122118")
    myroot.mainloop()
