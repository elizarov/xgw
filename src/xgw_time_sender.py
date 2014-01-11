import zigbee
from time import sleep, strftime
from xgw_worker import Worker
from xgw_xbee_map import str2addr


def fmt_time(secs):
    return 


TIMEOUT = 1;
TIME_SEND_PERIOD = 60  # 1 minute

class TimeSender(Worker):
    def __init__(self, xbee):
        Worker.__init__(self, name="TimeSender")
        self._xbee = xbee
    
    def work(self):
        sleep(TIME_SEND_PERIOD)
        print "xgw: Getting current destination address"
        addr = str2addr(zigbee.ddo_get_param(None, "DH", TIMEOUT) + zigbee.ddo_get_param(None, "DL", TIMEOUT))
        print "xgw: Sending time to %s" % (addr)
        self._xbee.send(strftime("[T: %y%m%d %H%M%S]\r\n"), addr)
