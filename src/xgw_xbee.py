"""XBee interface module for xgw"""

from socket import *
from collections import deque
from time import sleep
from threading import Thread
from xgw_xbee_map import to_addr, to_name_lazy

MAX_BUF = 10

ENDPOINT = 0xe8
PROFILE = 0xc105
CLUSTER = 0x11

class XBee(Thread):
    def __init__(self):
        Thread.__init__(self)
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
        self._sock.sendto(data, 0, (node, ENDPOINT, PROFILE, CLUSTER))
        
    def recv(self, src, wait=0, last=MAX_BUF):
        node = to_addr(src)
        sleep(int(wait))
        if node not in self._buf:
            return ""
        return "".join(list(self._buf[node])[-int(last):])

    def run(self):
        while not self._closed:
            data, addr = self._sock.recvfrom(255)
            node, endpoint, profile, cluster = addr[:4]
            other_addr = ""
            if endpoint == ENDPOINT and profile == PROFILE and cluster == CLUSTER:
                self.append(node, data)
            else:
                other_addr = " (" + hh(endpoint, 2) + "," + hh(profile, 4) + "," + hh(cluster, 2) + ")" 
            print "xgw: Recv ", to_name_lazy(node), other_addr, ": ", repr(data)
    
    def append(self, node, data):
        if node not in self._buf:
            self._buf[node] = deque()
        self._buf[node].append(data)
        if len(self._buf[node]) > MAX_BUF:
            self._buf[node].popleft()

#---- Utility methods ----  

def hh(s, n):
    return hex(s).replace('0x', '').zfill(n)
        