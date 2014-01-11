
from time import sleep, time
from xgw_worker import Worker
from xgw_data import CURRENT
from xgw_config import CONFIG

import digi_httplib as httplib
import sys
 
SLEEP_PERIOD  = 1            # 1 second
FETCH_MESSAGES_PERIOD = 60   # 1 minute
UPLOAD_DATA_PERIOD = 5 * 60  # 5 minutes
RETRY_PERIOD =  60           # 1 minute

class Uploader(Worker):
    def __init__(self, xbee):
        Worker.__init__(self, name="Uploader")
        self._xbee = xbee
        self._messages_session = None
        self._last_message_index = None
        now = time()
        self._next_data_time = now + RETRY_PERIOD
        self._next_messages_time = now 

    def work(self):
        sleep(SLEEP_PERIOD)
        # upload / fetch messages
        now = time()
        if CURRENT.urgent or now > self._next_messages_time or self._last_message_index:
            CURRENT.urgent = False
            success = self._uploadMessages(list(CURRENT.messages)) 
            if not success:
                CURRENT.urgent = True
            self._next_messages_time = now + FETCH_MESSAGES_PERIOD
        # upload urgent data        
        if CURRENT.urgent_data:
            data = CURRENT.urgent_data
            CURRENT.urgent_data = {}        
            success = self._uploadData(data.values())
            if not success:
                for (k, v) in data.iteritems():
                    if not v.sent and k not in CURRENT.urgent_data:
                        CURRENT.urgent_data[k] = v
        # upload regular (scheduled) data                
        now = time()
        if now > self._next_data_time:
            success = self._uploadData(CURRENT.data.values())
            if success:
                self._next_data_time = now + UPLOAD_DATA_PERIOD 
            else:
                self._next_data_time = now + RETRY_PERIOD
            
    def _uploadMessages(self, msg_values):
        msgs = []
        csvs = []
        now = time()
        for msg in msg_values:
            if not msg.sent:
                msgs.append(msg)
                csvs.append(msg.csv(now))
        bytes = "\r\n".join(csvs)
        url = CONFIG.MESSAGE_PATH + "?id=2"
        headers = {}
        if self._messages_session:
            headers["Cookie"] = self._messages_session
        else:
            url += "&newsession1"
        if self._last_message_index:
            url += "&index=" + str(self._last_message_index)    
        print "xgw: Sending %d messages to %s%s in %d bytes" % (len(msgs), CONFIG.HOST, url, len(bytes))
        ok, cookie, body = http("POST", url, bytes, headers) 
        if ok:
            self._messages_session = cookie
            self._last_message_index = None
            incoming_msgs = body.split("\r\n")
            for incoming_msg in incoming_msgs:
                if not incoming_msg:
                    continue
                print "xgw: Processing incoming message ", repr(incoming_msg)
                m = incoming_msg.split(",")
                if len(m) < 4:
                    continue
                text = m[1]
                self._last_message_index = int(m[3])
                self._xbee.send(text)
            for msg in msgs:
                msg.sent = True
            return True
        return False
        
    def _uploadData(self, data_values):
        datas = []
        csvs = []
        now = time()
        for data in data_values: 
            if not data.sent:
                datas.append(data)
                csvs.append(data.csv(now))
        if len(datas) == 0:
            return False # recheck in 1 min if nothing to send on periodic upload
        bytes = "\r\n".join(csvs)
        print "xgw: Sending %d data items to %s%s in %d bytes" % (len(datas), CONFIG.HOST, CONFIG.DATA_PATH, len(bytes))
        ok, cookie, body = http("PUT", CONFIG.DATA_PATH, bytes) 
        if ok:
            for data in datas:
                data.sent = True
            return True
        return False

def http(method, path, bytes, headers={}):
    try: 
        headers.update(CONFIG.AUTH)
        conn = httplib.HTTPConnection(CONFIG.HOST)
        conn.request(method, path, bytes, headers)
        resp = conn.getresponse()
        print "xgw: HTTP %d %s" % (resp.status, resp.reason)
        ok = resp.status == httplib.OK
        cookie = resp.getheader("Set-Cookie")
        body = resp.read()
        conn.close()
        return ok, cookie, body
    except:
        print "xgw: Unexpected HTTP exception", sys.exc_info()[0]    
        return False, None, None
