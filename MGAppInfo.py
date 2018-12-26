# Copyright @ 2018 Michael George
#
# MGAppInfo.py
#
# 2018-12-24  mg  application specific strings and identifiers
#

class mg_applicationinfo():
    def __init__(self):
        self.appname = 'MG File Utilities'
        self.appversionstring = 'Version 4.0'
        self.appcopyright = 'Copyright @ 2018  MICHAEL GEORGE'
        self.apprev = 4.0
        self.appdate =  '2018-12-24'

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
