import zigbee
from time import sleep, localtime, strftime
from xgw_worker import Worker
from xgw_xbee_map import str2addr

TIMEOUT = 1 

class TimeSender(Worker):
    def __init__(self, xbee):
        Worker.__init__(self, name="TimeSender")
        self._xbee = xbee
        self._last = ""
    
    def work(self):
        sleep(0.5) # makes sure we catch 00 seconds asap 
        time = localtime()
        if time.tm_sec != 0:
          return # wait for 00 seconds(!)
        if time.tm_year < 2000:
          return # wait until time sync   
        s = strftime("[T:%y-%m-%d %H:%M]\r\n", time)
        if s == self._last:
            return # this time was just sent
        self._last = s
        print "xgw: Getting current destination address"
        addr = str2addr(zigbee.ddo_get_param(None, "DH", TIMEOUT) + zigbee.ddo_get_param(None, "DL", TIMEOUT))
        print "xgw: Sending time %s to %s" % (repr(s), addr)
        self._xbee.send(s, addr)
