"""Controller for xgw commands"""

import sys

class Controller:
    def __init__(self, xbee):
        self._xbee = xbee
        
    def quit(self):
        self._xbee.close()
        sys.exit()
        
    def send(self, data, **args):
        self._xbee.send(unescape(data), **args)
        return "Sent: " + data
    
    def recv(self, **args):
        return self._xbee.recv(**args)
    
#---- Utility methods ----   

def unescape(data):
    return data.replace("\\r", "\r").replace("\\n", "\n")
