# Copyright @ 2018.2019 Michael George
#
# MGAppInfo.py
#
# 2018-12-24  mg  application specific strings and identifiers
# 2019-02-23 mg now includes COPY UNIQUE FILES TO NEW DRIVE or DELETE DUPs ON EXISTING DRIVE
# 2019-03-31 mg added stats for bl, wl, dirs, exts

class mg_applicationinfo():
    def __init__(self):
        self.appname = 'MG File Utilities'
        self.appversionstring = 'Version 4.32'
        self.appcopyright = 'Copyright @ 2018, 2019  Michael George'
        self.apprev = 4.1
        self.appdate =  '2019-03-31'

    def mg_getappversion(self):
        return self.appversionstring
    
    def mg_getappname(self):
        return self.appname
    
    def mg_getappcopyright( self):
        return self.appcopyright
    
    def mg_getappversionvalue(self):
        return self.apprev

    def mg_getappdate(self):
        return self.appdate


if __name__ == '__main__':
    myinf = mg_applicationinfo()
    print( myinf.mg_getappname(),
           myinf.mg_getappversion(),
           myinf.mg_getappcopyright(),
            myinf.mg_getappdate(),
           "%4.1f"% myinf.mg_getappversionvalue())
