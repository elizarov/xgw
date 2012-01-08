"""XBee interface module for xgw"""

from socket import *
from collections import deque
from time import sleep
from threading import Thread

MAX_BUF = 10
DEFAULT_DEST = "[00:00:00:00:00:00:FF:FF]!" # Broadcast


class XBee(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._sock = socket(AF_ZIGBEE, SOCK_DGRAM, ZBS_PROT_TRANSPORT)
        self._sock.bind(("", 0xe8, 0, 0))
        self._closed = False
        self._buf = {} # node -> messages
    
    def close(self):
        self._closed = True
        self._sock.close()
        self.join()

    def send(self, data, dest=DEFAULT_DEST):
        self._sock.sendto(data, 0, (dest, 0xe8, 0xc105, 0x11))
        
    def recv(self, src, wait=0, last=MAX_BUF):
        sleep(int(wait))
        if src not in self._buf:
            return ""
        return "".join(list(self._buf[src])[-int(last):])

    def run(self):
        while not self._closed:
            data, addr = self._sock.recvfrom(255)
            node = addr[0]
            self.append(node, data)
            print "xgw: Recv from %s: %s" % (node, repr(data))
    
    def append(self, node, data):
        if node not in self._buf:
            self._buf[node] = deque()
        self._buf[node].append(data)
        if len(self._buf[node]) > MAX_BUF:
            self._buf[node].popleft()
        