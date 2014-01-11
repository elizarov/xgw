"""Controller for xgw commands"""

import sys
from xgw_data import CURRENT

class Controller:
    def __init__(self, xbee, uploader):
        self._xbee = xbee
        self._uploader = uploader
        
    def send(self, data, **args):
        self._xbee.send(unescape(data), **args)
        return "Sent: " + data
    
    def recv(self, **args):
        return self._xbee.recv(**args)
    
    def data(self):
        result = ["\n"]
        for data in CURRENT.data.values(): # cannot use itervalues(), because it may change
            result.append(data.element())
            result.append("\n")
        return result        
    
    def messages(self):
        result = ["\n"]
        for msg in CURRENT.messages:
            result.append(msg.element())
            result.append("\n")
        return result        
    
#---- Utility methods ----   

def unescape(data):
    return data.replace("\\r", "\r").replace("\\n", "\n")
