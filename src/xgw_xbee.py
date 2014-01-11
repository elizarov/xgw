"""XBee interface module for xgw"""

from socket import *
from collections import deque
from time import sleep, time
from threading import Thread
from xgw_xbee_map import to_addr, is_addr
from xml_element import Element
from xgw_data import updateDataLine, updateDataItems
from time_util import fmt_time

from libs.xbeeprodid import GetXBeeProductName, XBeeSensorLTHAdapter
import libs.xbeelth as xbeelth

MAX_BUF = 30

# default XBee TTY endpoint/profile/cluster
ENDPOINT = 0xe8
PROFILE = 0xc105
TTY_CLUSTER = 0x11
IS_CLUSTER = 0x92

class XBee(Thread):
    def __init__(self, resolver):
        Thread.__init__(self, name="XBee")
        self._resolver = resolver
        self._sock = socket(AF_ZIGBEE, SOCK_DGRAM, ZBS_PROT_TRANSPORT)
        self._sock.bind(("", ENDPOINT, 0, 0))
        self._closed = False
        self._buf = {} # node -> messages
    
    def close(self):
        self._closed = True
        self._sock.close()
        self.join()

    def send(self, data, dest=""):
        node = to_addr(dest)
        self._sock.sendto(data, 0, (node, ENDPOINT, PROFILE, TTY_CLUSTER))
        
    def recv(self, src, wait=0, last=MAX_BUF):
        node = to_addr(src)
        sleep(int(wait))
        if node not in self._buf:
            return ""
        return list(self._buf[node])[-int(last):]

    def run(self):
        while not self._closed:
            data, addr = self._sock.recvfrom(255)
            node, endpoint, profile, cluster = addr[:4]
            cur_time = time()
            is_data = endpoint == ENDPOINT and profile == PROFILE and cluster == IS_CLUSTER
            node_name = self._resolver.to_name_non_blocking(node, is_data)
            data_name = "t"
            data_text = data
            data_attrs = dict(time=fmt_time(cur_time))
            other_addr = ""
            if endpoint == ENDPOINT and profile == PROFILE and cluster == TTY_CLUSTER:
                updateDataLine(node_name, data, cur_time)
            else:
                data_name = "h"
                data_text = str2hex(data)
                data_attrs["endpoint"] = hh(endpoint, 2)
                data_attrs["profile"] = hh(profile, 4)
                data_attrs["cluster"] = hh(cluster, 2)
                other_addr = " (" + data_attrs["endpoint"] + "," + data_attrs["profile"] + "," + data_attrs["cluster"] + ")"
                    
            self.append(node, Element(data_name, data_attrs, data_text))
            print "xgw: Recv ", node_name, other_addr, ": ", repr(data_text)
            if is_data and not is_addr(node_name):
                device_type, product_type = self._resolver.to_product_type_non_blocking(node)
                items = {}
                if product_type == XBeeSensorLTHAdapter:
                    items = xbeelth.sample(data)
                print "xgw: Recv ", node_name, " IS sample from ", GetXBeeProductName(product_type), " = ", repr(items)
                updateDataItems(node_name, items, cur_time)    
    
    def append(self, node, data):
        if node not in self._buf:
            self._buf[node] = deque()
        self._buf[node].append(data)
        if len(self._buf[node]) > MAX_BUF:
            self._buf[node].popleft()

#---- Utility methods ----  

def hh(s, n):
    return hex(s).replace('0x', '').zfill(n)

def str2hex(s):
    result = []
    for c in s:
        result.append(hh(ord(c), 2))
    return "".join(result)
    